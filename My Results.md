


---
## Q(a)
```
Går det snabbare att träna nätverken (i antalet epoker) om vi ökar inlärningshastigheten (lr) på nätverken?
Kan vi ha en för stor inlärningshastighet och vad händer då?
```
## Answer
```
Med en snabb inlärningstakt är det lättare att träna upp nätverken, men det finns risk att ta för många enorma steg, vilket minskar noggrannheten. Som ett resultat tar det längre tid att få en lika exakt modell.

lr 0,02, lr 0,7 och lr 1 jämförs.
Det tog längre tid för en modell med en inlärningshastighet på 0,02 att uppnå en hög noggrannhet till en början, och den var aldrig så exakt som de med 0,7 och 1 på 100 epoker. (figur 1)

Den roterade datan följde kurvan i figur 1, dock gjorde inte den förflyttade datan det.
```
![figur 1](/img/fig1.svg)


---

## Q(b)
```
Vad händer om vi minskar storleken på våra träningsbatcher (batch_size)? Hur ändras prestandarden och träningstiden?
```
## Answer
```
Vi märkte att modellen försämrades med tiden när batch_size = 6. Vi kom till slutsatsen att eftersom det finns nio (9) olika nummer och en batch_size på 9, kommer modellen inte att behöva träna på alla innan den uppdaterar sin vikter.
När varje (ofullständig) batch försöker uppdatera med stora steg, höjdes detta till allvarliga nivåer med lr = 0,7.

Efter att ha observerat med batch_size = 6 så experimenterade vi med batch_size = 45. 

Vi trodde att med en batch_size på 9 så skulle det finnas en större chans att få tag i varje siffra i varje batch och arbeta med dem innan uppdateringen av modellen sker.
Vår teori var helt rätt, modellen visar högre accurecy än storleken 6. Se figur 2.

Men när det gäller det gäller snabbheten så såg vi att en batch med size på 70 var snabbare än en modell med 140 då man kan se att den uppdaterar modellen mer ofta. När vi körde batch_size = 6 så tog det väldigt lång tid gämfört med batch_size = 45 det är på av att modellen behöver uppdatera sig aldeless för mycket och att det håller på inte att kunna träna alla innan den innan den uppdaterar sina vikter.

```
![batch size accuracies](/img/fig2.svg)
(figure 2)
---


## Q(c)
```
Hur skiljer de båda modellerna(Convolutional & non-convolutional) sig när det kommer till träningstid? Förklara lite kort om 
varför de skiljer sig åt.
```
## Answer
```
En convolutional är betydligt bättre på att överföra data eftersom det inte spelar någon roll var numret finns i bilden. 
Medan en icke faltningsmodell är bra på att lokalisera numret beroende på var pixlarna finns i bilden.
Eftersom convolutional delar upp bilden i mindre bilder som validerar, har faltning visat sig vara långsammare men mer exakt. Stegen är också sammanflätade. Istället för att röra sig direkt genom bilden, vilket är betydligt snabbare. 
```

---

## Q(d)
```
Hur skiljer sig resultatet mellan de olika testseten och varför kan vi se/inte se en skillnad?
Är det samma skillnader för båda närverken?
```
## Answer
```
convo = convolutional model
non_convo = non convolutional model
Moved Data:
Det finns en tydlig skillnad mellan convo och non convo. Convo har en högre noggrannhet, vilket vi tror beror på att den inte förlitar sig mycket på positionsförhållandet mellan pixlarna i hela bilden. Den fokuserar på att upptäcka mönster som pixlar oavsett var de befinner sig. 
Detta möjliggörs av de flera "träningspass" som talaren utför på olika delar av bilderna under sin träning.
Non convo, å andra sidan, utför ett "pass" där varje pixel tilldelas en neuron. Detta innebär att modellen åter bekantar sig med mönster i sammanhanget "den stora bilden". Som ett resultat, om siffrorna i bilden flyttas, blir det svårt att matcha pixlarna i förhållande till hela bilden och hitta rätt antal.
```
![Moved Data: non-convolutional](/img/fig3.png)(non-convolutional)
![Moved Data: convolutional](/img/fig4.png)(convolutional)

```
Rotated Data:
I den här situationen är nätverket väldigt likt. Siffrorna flyttas inte, därför förblir deras position i den övergripande bilden oförändrad. Behåll ett distinkt mönster för varje siffra, även om de alla är roterade.
```
![Rotated Data: non-convolutional](/img/fig5.png)(non-convolutional)
![Rotated Data: convolutional](/img/fig6.png)(convolutional)

---

```


