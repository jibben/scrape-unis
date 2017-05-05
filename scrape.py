import requests
import csv
from bs4 import BeautifulSoup

HTML = 'https://directory.columbia.edu/people/search'

DEPT_TO_FULL= {
        'BME' : 'Biomedical Engineering',
        'CS' : 'Computer Science',
        'IEOR' : 'Industrial Engineering & Operations Research',
        'ChemE' : 'Chemical Engineering',
        'MechE' : 'Mechanical Engineering',
        'EEE' : 'Earth and Environmental Engineering',
        'Civil' : 'Civil Engineering',
        'APAM' : 'Applied Physics and Applied Mathematics',
        'EE' : 'Electrical Engineering',
        'BME' : 'Biomedical Engineering',
}


def get_page(name, dept=None):

    #payload = {'filter.searchTerm' : name, 'filter.title' : 'fu'}
    payload = {'filter.searchTerm' : name}

    if dept and dept in DEPT_TO_FULL:
        payload['filter.department'] = DEPT_TO_FULL[dept]

    r = requests.post(HTML, payload)

    return r.text


def parse_emails(page):
    soup = BeautifulSoup(page, 'lxml')

    mailtos = soup.findAll('a', {'class' : 'mailto'})

    return [mt.get_text() for mt in soup.findAll('a', {'class' : 'mailto'})]


def get_email(name, dept=None):
    page = get_page(name, dept)
    return parse_emails(page)

def get_names(csv_filename):
    names = []
    with open(csv_filename, 'r') as csvf:
        reader = csv.reader(csvf)
        next(reader) # skip header
        for line in reader:
            names.append(' '.join([line[1], line[0]]))

    return names


names = get_names('names.csv')

i = 0
with open('emails.txt', 'w') as fout:
    for name in names:
        fout.write(','.join(get_email(name)))
        fout.write('\n')
        i += 1
        if i % 20 == 0:
            print(i)
