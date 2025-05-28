import requests
import json 
import csv 

url = "https://bizfileonline.sos.ca.gov/api/Records/businesssearch"

payload = json.dumps({
  "SEARCH_VALUE": "1",
  "SEARCH_FILTER_TYPE_ID": "0",
  "SEARCH_TYPE_ID": "1",
  "FILING_TYPE_ID": "",
  "STATUS_ID": "",
  "FILING_DATE": {
    "start": None,
    "end": None
  },
  "CORPORATION_BANKRUPTCY_YN": False,
  "CORPORATION_LEGAL_PROCEEDINGS_YN": False,
  "OFFICER_OBJECT": {
    "FIRST_NAME": "",
    "MIDDLE_NAME": "",
    "LAST_NAME": ""
  },
  "NUMBER_OF_FEMALE_DIRECTORS": "99",
  "NUMBER_OF_UNDERREPRESENTED_DIRECTORS": "99",
  "COMPENSATION_FROM": "",
  "COMPENSATION_TO": "",
  "SHARES_YN": False,
  "OPTIONS_YN": False,
  "BANKRUPTCY_YN": False,
  "FRAUD_YN": False,
  "LOANS_YN": False,
  "AUDITOR_NAME": ""
})
headers = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9',
  'authorization': 'undefined',
  'content-type': 'application/json',
  'origin': 'https://bizfileonline.sos.ca.gov',
  'priority': 'u=1, i',
  'referer': 'https://bizfileonline.sos.ca.gov/search/business',
  'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
  'Cookie': 'visid_incap_2299457=BiLaiu6RTDWnjxYw1IRkMFRsNmgAAAAAQUIPAAAAAAAmbJ5rURQNrW6ou7Z3MiwX; nlbi_2299457=9QFpDytxBlj5KqJLyPrJvAAAAAAC1Jo96mRedOsjvMhwdwFV; incap_ses_1633_2299457=i3XlJax50wcOvxqVKpWpFlRsNmgAAAAAZ/HkQycOwER4vHVSQqM14w==; ASP.NET_SessionId=gl1cbtchmdf4j250yhrlvnij; reese84=3:wjSnKZANikGqWyu5mUnVew==:RFTOicp4mLYi08+zAMTobFAhcPedgpGxxBs/kwNIUuq7J8x1baGak6mA1QcqgjElCu75u7D3dQRFd+kHN9CU8PvJ5MYYZnkMfgHV0G2ZSgJgumVU4QwhgIz9ibMC2OOHREFk/Glf34viIQFbPfboAj9JmqWRptX/QBmKJGR54d8lzj3sACUibcoRQ160yYy4+tAlDA4VnMpHTmgZbWx+TNNjPszPmtpPxbyRSwom4JDRRWI45Vds1APmGpaflRUvnNriU60K1GFHvXX/YjGFVidylNDPOu3sBc5gybhjbNg3hoLd3tSQxeInkEN/hb9g295R1Z837fGVSN9+SWhG51+Q3/1JbPxohtZorU+EII+zQOb7gdXP5iW29ukmTWxZNC49TNOYULqZTvY9TOwO7jxyPGhtPBQnmToXq0yBGIp+CIblaMeCpT08U5WONVTXWf94qvcYc/cGgEFgP1WCUA==:8aWdLtgNmUBB2ZUSZmEmQCyYqF1yTD4/xCQf2rFCxvE=; nlbi_2299457_2147483392=8b7AYko3j0XFFJyhyPrJvAAAAABWsBFO6Wn/FwreZp9wxlpe'
}

response = requests.request("POST", url, headers=headers, data=payload)


if response.status_code == 200:
    data = response.json()
    rows = list(data['rows'].values())
    # load raw data
    with open('raw_list.csv', 'w') as f:
      fieldnames = rows[0].keys()
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(rows)

    # load data using template
    fieldname_ids = [i['id'] for i in data['template']]
    fieldnames = [i['label'] for i in data['template']]
    rows = list(data['rows'].values())
    with open('templated_data_list.csv', 'w', newline='') as file: 
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        for row in rows:
          filtered_row = {key: row.get(key, '')[0] if key == 'TITLE' else row.get(key, '') for key in fieldname_ids}
          writer.writerow(filtered_row.values())



print('scrape done')
