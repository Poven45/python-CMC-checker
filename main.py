import bs4
import requests
import smtplib
dialogue = ("Enter cryptos you want to know the price of\n"
            "If there are multiple coins/tokens then do this:\n"
            "(Start with your first coin)Ex: bitcoin, shiba inu, polygon, titano, etc\n"
            "Then just hit enter:\n")
cryptoSend = ""
# The email you want to use to send emails to yourself, can be the same one
# YOU NEED A APP SPECIFIC PASSWORD: https://support.google.com/accounts/answer/185833?hl=en
email = ""
emailPassword = ""
# The email you want to be able to receive emails for updates
emailRec = ""
# The smtp for your email provider, followed by port number
# ex: "smtp.gmail.com", "smtp.mail.yahoo.com", smtp-mail.hotmail.com
# may need to change this to your email port number for smtp
emailServer = smtplib.SMTP('smtp.gmail.com', 587)
type(emailServer)
# starts connection
emailServer.ehlo()
# encryption
emailServer.starttls()
emailServer.login(email, emailPassword)

emailSubject = 'Subject: Here is your crypto update! \n\n'

# input the coins/tokens below that you want to see
# cryptos = "bitcoin, polygon, shiba inu"
cryptos = input(dialogue)
crypto = cryptos.split(", ")

site = "https://coinmarketcap.com/currencies/"
# crypto = crypto.replace(" ", "-")
# if(crypto[-1] == " "):
#     crypto = crypto[:-1]
# elif(crypto[-1] == "-"):
#     crypto = crypto[:-1]
counter = 0
# Suffix and prefix removal requires python 3.9+
for i in range(len(crypto)):

    crypto[i] = crypto[i].replace(" ", "-")
    crypto[i] = crypto[i].removeprefix("-")
    crypto[i] = crypto[i].removeprefix("--")
    crypto[i] = crypto[i].removesuffix("-")
    crypto[i] = crypto[i].removesuffix("--")
    counter = counter + 1

counter = 0
cryptoSite = []
for i in crypto:
    cryptoSite.append(site + crypto[counter] + "/")
    counter = counter + 1

counter = 0
for i in cryptoSite:
    req = requests.get(cryptoSite[counter])
    req.status_code
    req.raise_for_status()

    parse = bs4.BeautifulSoup(req.text, 'html.parser')

    element = parse.select('#__next > div > div.main-content > div.sc-1a736df3-0.PimrZ.cmc-body-wrapper > div > div.sc-aef7b723-0.jfPVkR.container > div.sc-ae09f8f5-0.dshRSa > div > div.sc-aef7b723-0.dDQUel.priceSection > div.sc-aef7b723-0.dDQUel.priceTitle > div > span')
    percentChange = parse.select('#__next > div.sc-c5c9d167-1.bLOtNZ > div.main-content > div.sc-1a736df3-0.PimrZ.cmc-body-wrapper > div > div.sc-aef7b723-0.jfPVkR.container > div.sc-ae09f8f5-0.dshRSa > div > div.sc-aef7b723-0.dDQUel.priceSection > div.sc-aef7b723-0.dDQUel.priceTitle > span')
    upOrDown = parse.select('#__next > div.sc-c5c9d167-1.bLOtNZ > div.main-content > div.sc-1a736df3-0.PimrZ.cmc-body-wrapper > div > div.sc-aef7b723-0.jfPVkR.container > div.sc-ae09f8f5-0.dshRSa > div > div.sc-aef7b723-0.dDQUel.priceSection > div.sc-aef7b723-0.dDQUel.priceTitle > span > span')

    if(str(upOrDown[0]) == '<span class="icon-Caret-down"></span>'):
        upOrDown[0] = 'Down'
    elif(str(upOrDown[0]) == '<span class="icon-Caret-up"></span>'):
        upOrDown[0] = 'Up'
    price = str(element[0].text)
    price = price[1:]
    price = price.replace(',', '')
    percent = str(percentChange[0].text)
    percent = percent[:-1]
    change = (float(price) / 100.0) * float(percent)
    change = str(f'{change:.8f}')
    changeCheck = str(change)

    if(changeCheck[0] == '0' and upOrDown[0] == 'Down'):
        print(f'{crypto[counter]} is {element[0].text}. It is {upOrDown[0]} {percentChange[0].text}(-{change} cents) in 24hrs')
        cryptoSend = cryptoSend + (
            f'{crypto[counter]} is {element[0].text}. It is {upOrDown[0]} {percentChange[0].text}(-{change} cents) in 24hrs')
    elif(changeCheck[0] == '0' and upOrDown[0] == 'Up'):
        print(f'{crypto[counter]} is {element[0].text}. It is {upOrDown[0]} {percentChange[0].text}(+{change} cents) in 24hrs')
        cryptoSend = cryptoSend + (
            f'{crypto[counter]} is {element[0].text}. It is {upOrDown[0]} {percentChange[0].text}(+{change} cents) in 24hrs')

    if(changeCheck[0] != '0' and upOrDown[0] == 'Down'):
        print(f'{crypto[counter]} is {element[0].text}. It is {upOrDown[0]} {percentChange[0].text}(-{change} dollars) in 24hrs')
        cryptoSend = cryptoSend + (
            f'{crypto[counter]} is {element[0].text}. It is {upOrDown[0]} {percentChange[0].text}(-{change} dollars) in 24hrs')
    elif(changeCheck[0] != '0' and upOrDown[0] == 'Up'):
        print(f'{crypto[counter]} is {element[0].text}. It is {upOrDown[0]} {percentChange[0].text}(+{change} dollars) in 24hrs')
        cryptoSend = cryptoSend + (
            f'{crypto[counter]} is {element[0].text}. It is {upOrDown[0]} {percentChange[0].text}(+{change} cents) in 24hrs')
    counter = counter + 1
    cryptoSend = cryptoSend + '\n' + '\n'
# from goes first, then to
emailServer.sendmail(email, emailRec, emailSubject + cryptoSend)
