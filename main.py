import requests as req

# EDGAR api root
root = "https://data.sec.gov/"

# for some reason this user agent works-im not asking questions ¯\_(ツ)_/¯
headers = {
    'User-Agent': 'Sample Company Name AdminContact@<sample company domain>.com',
}

ticker = []

# read ticker.txt to be used later in @get_company_by_ticker
with open("assets/ticker.txt", "r") as f:
    ticker = f.readlines()
    f.close()

# returns: the json string with all the data about a company
# param {cik}: the Central Index Key corresponding to a certain company
# example cik: '320193' for apple
def get_company_by_cik(cik):
    # apparently there's a hidden end of line character or some shit like that, so you have
    # to strip the string beforehand. python smh this wouldn't happen in java
    # cik has to have zeros in the beginning to reach length of 10, e.g. 320193 -> 0000320193
    cik = cik.strip().zfill(10)
    # headers are the cors shit so that sec doesn't act like a bitch
    return req.get(root+f"submissions/CIK{cik}.json", headers=headers).text

# just like @get_company_by_cik but accepts the ticker of a company instead of CIK
# example ticker: 'aapl' for apple
def get_company_by_ticker(tick):
    for line in ticker:
        if tick.lower() in line:
            return get_company_by_cik(line[line.find('\t') + 1:])


# test code
out = get_company_by_ticker("aapl")

with open("out.json", "w") as f:
    f.write(out)
    f.close()
