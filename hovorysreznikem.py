from requests_html import HTMLSession
from unidecode import unidecode 
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


session= HTMLSession()
stranka = session.get("https://eshop.kucharkaprodceru.cz/kucharky/")

stranka.html.render(sleep = 5)

kucharka = stranka.html.find(".pagination-description-total")
kucharka2 = stranka.html.find('.p-name')

soubor = open('kucharka_1.txt', "r", encoding = "utf-8")
pocet_titulu_stranka = [pocet.text for pocet in kucharka]
diakritika = [unidecode(x).split(",") for x in pocet_titulu_stranka]
pocet_polozek = "".join(diakritika[0])
nazvy_kucharek_stranka = [name.text for name in kucharka2]
diakritika2 = [unidecode(x) for x in nazvy_kucharek_stranka]
obsah_s = [x.strip("\n") for x in soubor]
soubor.close()

nove_pridane_t = []

for konkretni_titul in diakritika2:
  if konkretni_titul not in obsah_s:
    nove_pridane_t.append(konkretni_titul)

spojene_tituly = ",".join([x for x in nove_pridane_t])

soubor = open('kucharka_1.txt', "a", encoding = "utf-8")
[soubor.write(nove_pridane+ "\n") for nove_pridane in nove_pridane_t]
soubor.close()

if len(nove_pridane_t) > 0: #podminka, kdy se ma posilat email 

  s = smtplib.SMTP("smtp.web4u.cz", 587)
  s.ehlo()

  with open(r'C:\Users\Jana.DESKTOP-0VR89AP\Desktop\kucharka.txt', 'r') as f:
    password = f.read()


  msg= MIMEText(f"Nove pridane tituly: {spojene_tituly},\nPocet titulu na strance: {pocet_polozek}")
  msg['Subject'] = 'Kucharka pro dceru'
  msg['From'] = 'jankakorycanova@kucharkaprodceru.cz'
  msg['To'] = 'janakorycanova@gmail.com'
  s.login("info@janadev.cz", password)
  s.sendmail(msg['From'],msg['To'],msg.as_string())
  s.quit()











