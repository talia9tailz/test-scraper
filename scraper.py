import requests, csv

# obtain input spreadsheet
input_sheet = requests.get('https://docs.google.com/spreadsheets/d/1H1a9eBamflt3w-4BPEk1kJYc4VgsDBWlDjkS0hV5tAY/export?format=csv')
f = open('input.csv', 'wb')
f.write(input_sheet.content)
f.close()
# create output spreadsheet
f = open('output.csv', 'w')
f.write('')
f.close()

# open spreadsheet
with open('input.csv', newline='') as f_in:
    reader = csv.reader(f_in)
    # initialize iteration counter
    n = 0
    # iterate over rows in sheet
    for row in reader:
        # process header row
        if n == 0:
            row.append('Valid')
        # process data rows
        else:
            # format request
            data = { 'address1': row[1], 'zip': row[4] }
            headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0' }
            url = 'https://tools.usps.com/tools/app/ziplookup/zipByAddress'
            # request address lookup through USPS
            r = requests.post(url=url, headers=headers, data=data)
            # determine address validity
            if 'ADDRESS NOT FOUND' in r.text:
                row.append('False')
            else:
                row.append('True')
        # write to output sheet
        with open('output.csv', 'a', newline='') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(row)
        # increment iteration counter
        n+=1
