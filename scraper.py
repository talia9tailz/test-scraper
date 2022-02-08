import requests, csv

# obtain input spreadsheet
input_sheet = requests.get('https://docs.google.com/spreadsheets/d/1H1a9eBamflt3w-4BPEk1kJYc4VgsDBWlDjkS0hV5tAY/ex
port?format=csv')
f = open('input.csv', 'wb')
f.write(input_sheet.content)
f.close()
# create output spreadsheet
f_out = open('output.csv', 'w')
f_out.write('')
f_out.close()
# open input sheet
with open('input.csv', newline='') as f_in:
    reader = csv.reader(f_in)
    # open output sheet in append mode
    with open('output.csv', 'a', newline='') as f_out:
        writer = csv.writer(f_out)
        # process header row
        header_row = next(reader)
        header_row.append('Valid')
        writer.writerow(header_row)
        # prepare request
        headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0' }
        url = 'https://tools.usps.com/tools/app/ziplookup/zipByAddress'
        # iterate over rows in sheet
        for row in reader:
            # format request
            data = { 'address1': row[1], 'zip': row[4] }
            # request address lookup through USPS
            r = requests.post(url=url, headers=headers, data=data)
            # check response code
            if str(r) == '<Response [200]>':
                # determine address validity
                if 'ADDRESS NOT FOUND' in r.text:
                    row.append('False')
                else:
                    row.append('True')
            else:
                row.append(r)
                # write to output sheet
            writer.writerow(row)
