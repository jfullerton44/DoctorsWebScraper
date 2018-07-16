from bs4 import BeautifulSoup
from requests import get
from time import time, sleep
from random import randint
import pandas as pd


names = []
specialties = []
affiliations = []

start_time = time()
requests = 0

info = {}

pages = [str(i) for i in range(1, 677)]

i = 1
# while i < 677:

# url = ('https://physician-finder.partners.org/search?page=' + str(i))
allNames=[]
allSpecialties=[]
allAffiliations=[]

while i< 5:
    url = ('https://physician-finder.partners.org/search?page='+ str(i))

    response = get(url)

    sleep(randint(1,3))

    requests += 1
    elapsed_time = time() - start_time
    current_time = time()
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
    #clear_output(wait=True)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    type(html_soup)

    containers = html_soup.find_all('div', class_='col-xs-8 col-sm-9')
    num_people = len(containers)
    p=0
    while p<num_people:
        person = containers[p]

        full_name = person.h2.a.text

        specialtyf = person.find('ul', class_="list-m no-bullets specialties.specialty-values")
        if specialtyf:
            specialties = specialtyf.getText(separator=u', ')

        affiliationf = person.find('ul', class_="list-m no-bullets network_affiliations.name-values")
        if affiliationf:
            affiliations = affiliationf.getText(separator=u'')


        allNames.append(full_name)
        allSpecialties.append(specialties)
        allAffiliations.append(affiliations)
        p=p+1
    i = i + 1


print(allNames,"\n")
print(allSpecialties,"\n")
print(allAffiliations,"\n")
doctors = pd.DataFrame({
    "name":allNames,
    "specilities": allSpecialties,
    "affiliation": allAffiliations
})
print(doctors.info())
doctors.to_csv('doctorsShort.csv')


