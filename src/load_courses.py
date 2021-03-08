import urllib.request
from bs4 import BeautifulSoup
from configparser import ConfigParser
import pymysql


def get_config(fn):
    parser = ConfigParser()
    parser.read(fn)
    db = parser.items('db')
    return {name: value for name, value in db}

def get_conn(conf):
    conn = pymysql.connect(**conf, cursorclass=pymysql.cursors.DictCursor)
    return conn

def insert_course(conn, course_number, semester, alt_req, class_name, level, professor_name, meet_time, room, desc):
    cursor = conn.cursor()
    q = 'INSERT INTO courses VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(q, (course_number, semester, alt_req, class_name, level, professor_name, meet_time, room, desc))
    conn.commit()

conf = get_config('/home/mzv205/csci60-hw07/config.ini')
conn = get_conn(conf)
print(conf)

urlfall2020 = "https://cs.nyu.edu/dynamic/courses/schedule/?semester=fall_2020"
urlspring2021 = "https://cs.nyu.edu/dynamic/courses/schedule/?semester=spring_2020"
pages = [urlfall2020, urlspring2021]

html = []
for p in pages:
    response = urllib.request.urlopen(p)
    html.append(response.read().decode('utf-8'))

courses = []
classes = []
count = 0
for h in html:
    dom = BeautifulSoup(h, features='html.parser')
    class_list = dom.select_one('ul.schedule-listing').select('li.row')
    if count == 0:
        semester = "FALL2020"
    else:
        semester = "SPRING2020"
    for each_row in class_list:
        spans = each_row.select('div span')
        course_number = (spans[0].get_text().split()[0])

        if course_number[-12] == 'U':
            level = 'UA'
        elif course_number[-12] == 'G':
            level = 'GA'
        else:
            level = 'NULL'

        if len(spans[0].get_text().split()) == 3:
            alt_req = (spans[0].get_text().split()[1])
        else:
            alt_req = "NULL"
        class_name = " ".join(spans[1].a.get_text().split())
        professor_name = spans[2].get_text().strip()
        professor_name = professor_name.split('\n')[0]
        meet_time = spans[3].get_text()
        room = spans[4].get_text().strip()
        desc = spans[-1].get_text().strip().split('\n')[0]

        if room == "":
            room = "NULL"

        insert_course(conn, course_number, semester, alt_req, class_name, level, professor_name, meet_time, room, desc)
        classes.append([course_number, semester, alt_req, class_name, level, professor_name, meet_time, room, desc])
    courses.append(classes[:])
    classes.clear()
    count = count+1

#
# for x in courses:
#     print(x)
#     print("SPRINGGGGGGG")
#     print("SPRINGGGGGGG")
#     print("SPRINGGGGGGG")
#     print('\n')
