from bs4 import BeautifulSoup
from requests import get
from time import time, sleep
from random import randint
import pandas as pd
import pymongo
import credentials


client = pymongo.MongoClient("mongodb+srv://"+credentials.username+":"+credentials.password+"@cluster1-xkuyo.mongodb.net/scrapedata?retryWrites=true")
db = client['scrapedata']
doctors = db.doctors
names = []
specialties = []
affiliations = []

start_time = time()
requests = 0

info = {}
i = 1
allNames = []
allSpecialties = []
allAffiliations = []
first_names = []
last_names = []
full_names = []
degrees = []
emails = []

while i < 677:
    url = ('https://physician-finder.partners.org/search?page='+ str(i))

    response = get(url)

    # sleep(randint(1, 3))

    requests += 1
    elapsed_time = time() - start_time
    current_time = time()
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
    html_soup = BeautifulSoup(response.text, 'html.parser')
    type(html_soup)

    containers = html_soup.find_all('div', class_='col-xs-8 col-sm-9')
    num_people = len(containers)
    p = 0
    while p < num_people:
        email=""
        person = containers[p]

        full_name = person.h2.a.text
        fname = full_name.split(',')
        degree = full_name.split(',', 1)[-1]
        full_name = fname[0]

        full_name = full_name.replace(',', '')
        sec = full_name.strip().split(' ')
        lensec = len(sec)
        first_name = sec[0]
        last_name = sec[lensec - 1]
        email = email + first_name[:1]
        email = email + last_name
        email = email + "@partners.org"

        specialtyf = person.find('ul', class_="list-m no-bullets specialties.specialty-values")
        if specialtyf is not None:
            specialties = specialtyf.getText(separator=u', ')
        else:
            specialties=""

        affiliationf = person.find('ul', class_="list-m no-bullets network_affiliations.name-values")
        if affiliationf is not None:
            affiliations = affiliationf.getText(separator=u'')
        else:
            affiliations = ""

        if doctors.find_one({"Full Name": full_name}, {"Email": email}) is not None:
            pass
        else:
            print("Creating Doctor: ", full_name)
            doctor = {
                "Full Name": full_name,
                "First Name": first_name,
                "Last Name": last_name,
                "Email": email,
                "Specialties": specialties,
                "Affiliations": affiliations
            }
            result = doctors.insert_one(doctor)
        p = p+1
    i = i + 1


print(allNames,"\n")
print(allSpecialties, "\n")
print(allAffiliations, "\n")
doctors = pd.DataFrame({
    "First Name": first_names,
    "Last Name": last_names,
    "Email": emails,
    "Full Name": full_names,
    "Specialities": allSpecialties,
    "Affiliation": allAffiliations
})
doctors = doctors[['First Name', 'Last Name', 'Email','Full Name', 'Specialities', 'Affiliation']]
print(doctors.info())
doctors.to_csv('doctorsFull.csv')


