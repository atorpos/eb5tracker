import requests
import time
import json
import re
from bs4 import BeautifulSoup

s = requests.session()
req_string = 'Case Was Approved'
i_526list = []

with open('eb5table.json', 'r') as myfile:
    data = myfile.read()
obj = json.loads(data)

for item in obj:
    case_no = item['case_id']
    print(case_no)

    url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
    request_payload = {'completedActionsCurrentPage': '0', 'upcomingActionsCurrentPage': '0',
                       'appReceiptNum': case_no, 'caseStatusSearchBtn': 'CHECK STATUS'}
    data = s.post(url, data=request_payload, headers={'Regerer': 'Origin: https://egov.uscis.gov'})

    soup = BeautifulSoup(data.text, 'html.parser')
    find_text = soup.find("h1")
    read_text = find_text.find_next_sibling("p").text.strip()
    if req_string in find_text.text:
        string_array = read_text[3:].split(",")
        date_record = string_array[0] + string_array[1]
        add_data = {
            "file_no": case_no,
            "case_status": find_text.text,
            "case_date": date_record
        }
        i_526list.append(add_data)
        print(add_data)
    else:
        continue
    time.sleep(0.5)
json_encode = json.dumps(i_526list, ensure_ascii=False)
print(json_encode)
file_name = 'i526update_' + case_no + str(time.time()) +'.json'
writefile = open(file_name, "x")
writefile.write(json_encode)
exit()