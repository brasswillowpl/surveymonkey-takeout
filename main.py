# licensed under "BSD"

import http.client
import json
import csv
import unidecode
import time

conn = http.client.HTTPSConnection("api.surveymonkey.com")

headers = {
    'Accept': "application/json",
    'Authorization': "Bearer APIKEY"

}

conn.request("GET", "/v3/surveys?per_page=500", headers=headers)

res = conn.getresponse()
data = res.read()

surveys = json.loads(data.decode("utf-8"))

count = 0

for survey in surveys["data"]:
    count+=1
    if count == 499:
        print("Daily Quota exceeded Soft limit 500")
    if count > 749:
        print("Daily Quota exceeded")
        print("Sleeping for 24 hours")
        time.sleep(86400)
        count = 0
    fields = ["Collector ID","Start Date","End Date","IP Address","Email Address","First Name","Last Name"]
    rows = []

    # conn.request("GET", "/v3/surveys/" +
    #              survey["id"]+"/responses", headers=headers)

    # res = conn.getresponse()
    # data = res.read()

    # survey_response = json.loads(data.decode("utf-8"))

    conn.request("GET", "/v3/surveys/" +
                 survey["id"]+"/details", headers=headers)

    res = conn.getresponse()
    data = res.read()

    survey_details = json.loads(data.decode("utf-8"))

    for page in survey_details["pages"]:
        for question in page["questions"]:
            fields.append(unidecode.unidecode(question["headings"][0]["heading"]))

    conn.request("GET", "/v3/surveys/" +
                 survey["id"]+"/responses/bulk?per_page=500", headers=headers)
    res = conn.getresponse()
    data = res.read()

    response_ids = json.loads(data.decode("utf-8"))

    for response in response_ids["data"]:
        # conn.request(
        #     "GET", "/v3/surveys/"+survey["id"]+"/responses/"+response["id"]+"/details", headers=headers)

        # res = conn.getresponse()
        # data = res.read()

        # survey_response_details = json.loads(data.decode("utf-8"))
        for page in response["pages"]:
            row = []
            row.append(response["collector_id"])
            row.append(response["date_created"])
            row.append(response["date_modified"])
            row.append(response["ip_address"])
            row.append(response["first_name"])
            row.append(response["last_name"])
            for question in page["questions"]:
                for answer in question["answers"]:
                    if "text" in answer:
                        row.append(answer["text"])
                    if "choice_metadata" in answer:
                        row.append(answer["choice_metadata"]["weight"])
            row = rows.append(row)
    try:
        with open("./"+unidecode.unidecode(survey["title"].replace("/", ""))+".csv", 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(fields)

            # writing the data rows
            csvwriter.writerows(rows)
    except Exception as e:
        print("error ", str(e))
