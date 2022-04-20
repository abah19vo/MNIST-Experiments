


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
Moved Data:
Det finns en tydlig skillnad mellan convolutional model och non convolutional model. convolutional model har en högre noggrannhet, vilket vi tror beror på att den inte förlitar sig mycket på positionsförhållandet mellan pixlarna i hela bilden. Den fokuserar på att upptäcka mönster som pixlar oavsett var de befinner sig. 
Detta möjliggörs av de flera "träningspass" som talaren utför på olika delar av bilderna under sin träning.
Non convolutional model, å andra sidan, utför ett "pass" där varje pixel tilldelas en neuron. Detta innebär att modellen åter bekantar sig med mönster i sammanhanget "den stora bilden". Som ett resultat, om siffrorna i bilden flyttas, blir det svårt att matcha pixlarna i förhållande till hela bilden och hitta rätt antal.
```
![Moved Data: non-convolutional](/img/fig3.png)(non-convolutional) ![Moved Data: convolutional](/img/fig4.png)(convolutional)


```
Rotated Data:
I den här situationen är nätverket väldigt likt. Siffrorna flyttas inte, därför förblir deras position i den övergripande bilden oförändrad. Behåll ett distinkt mönster för varje siffra, även om de alla är roterade.
```
![Rotated Data: non-convolutional](/img/fig5.png)(non-convolutional)
![Rotated Data: convolutional](/img/fig6.png)(convolutional)

---
## Q(e)
```
Vad händer om vi ökar antalet neuroner. Får vi ett bättre eller sämre resultat. Finns det 
någon undre eller övre gräns för vad som är bäst?
```
## Answer
```
Ju mer nueroner det finns i ett lager desto bättre blir accuracy men kosekvenserna ligger i tiden.

Resultat av Average Accuracy av olika neuroner:
     - 4 neuroner: 84 (23s)
     - 8 neuroner: 93 (20s)
     - 16 neuroner: 100 (23s)
     - 32 neuroner: 103.19 (24s)
     - 64 neuroner: 103.69 (25s)
     - 512 neuroner: 110.99 (1m )
     - 1024 neuroner: 110.99 (2m 20s)
```
---

## Q(f)
```
Öka området som analyseras åt gången med vårt ”convolutional neural network” (detta 
görs genom att öka värdet på vår kernel_size) och öka även storleken på stegen mellan 
varje yta som analyseras ” (detta görs genom att öka värdet på strides). Hur stora värden 
går det att ha på dessa parametrar innan prestandan börjar att sjunka. Vilka var de bästa 
värdena som du observerade? 
```
## A(f)
```
kernel_size = (16, 16) strides=(1, 1) är vårt första test istället för kernel_size = (8,8) . Eftersom rutnätinmatningen till neuronerna är 16x16 snarare än 8x8, minskar noggrannheten när mönstren blir bredare och matchar med fler siffror.

kernel_size=(8, 8) med strides=(3, 3) är vårt andra försök. Accuracyn minskade med bara 1% och tiden sänktes med 60%.

kernel_size=(8, 8) med strides=(8, 8) är vårt tredje försök. det var chockande att hitta ett dramatiskt lågt accrucy värde.
 
```

## Q(g)
```
Lägg till fler lager och testa om det blir bättre med djupare nätverk. Hur påverkas 
precisionen och träningstiden?
```
## A(g)

- testade först med non_convolutional_model:

| layers      | time (min:sec)    | accrucy rotated     | accrucy moved|
| ----------- | ----------- | ----------- | ----------- |
| 1    | 2:10 |  79.27  | 16.39  |
| 4    | 2:37 |  72.8   | 14.58  |
| 16   | 3:23 |  11.35  | 11.35  |
| 23   | 6:18 |  9.79   | 11.35  |


---

- vi testade sen med convolutional_model:

| layers      | time (min:sec)    | accrucy rotated     | accrucy moved|
| ----------- | ----------- | ----------- | ----------- |
| 1    | 2:20 |  46.7   | 17.96  |
| 4    | 2:20 |  56.49  | 20.23  |
| 8    | 2:20 |  54.55  | 18.63  |
| 12   | 2:20 |  51.51  | 18.34  |

```
Slutsats:
På non-cono så ökade tiden kraftigt med antalet lager men det betyder inte att det gick så bra för epoch accurucy. Men shockande i vanliga convolutional model så ändrades inte tiden men däremot så ökade accurucien till en viss grad sen började den sänka sig efter direkt efter fyra och 8 lager
     
```
---


# Egna Experment
```
Kör minst 5 st egna experiment med syftet att uppnå så bra precision på de tre olika testdataseten. 
Som ett sekundärt mål så ska det också gå så snabbt (mätt i sekunder) att träna nätverket. Använd 
det du har observerat under dina experiment i uppgift 7 för att skapa en så bra modell som möjligt. 
För varje experiment så ska du ge en kort beskrivning av vad det är du testar och varför du valde 
att testa just den givna parameterinställningen. 
```
## Experement 1
```

Testar med mindre epochs nu så jag sänker ner dem från 100 -> 50 
samt så sänker jag ner batch size till 9*3 för att vi märkte att när batchsizen är delbar med antalet figurer så får vi bättre resultat. 
Jag kommer kommer att sänka sätta neuroner till 128 i non covo modellen. 

resultatet var shockande för någon orsak
```     
- time: 10min, 38sek
- moved data: 15.73
- rotated data: 80.2
- test data:95.87

## Experement 2
```

Jag ändrar batchsizen till 9*15 så jag minimerar tiden, samma händer för lr jag ändrar den till 0.5

resultatet var shockande mindre för pga av att jag hade hade lika mycket neuroner men högre batchsize.  resultatet kom bättre från alla håll.
```
- time: 2 min, 47sek
- moved data: 17.73
- rotated data: 85.93
- test data: 97.84


## Experement 3
```

Jag ändrar batchsizen till 9*15 så jag förbättrar tiden, samma händer för lr jag ändrar den till 0.5. för att göra det mer intressant jag ändrar antalet neuroner till 640 för att göra expermentet mer intressant och för att se om det kommer att påverka possetivt eller negatitv

resultatet var bra för time, test data, rotated data men det sänkte väldigt mycket när det gäller moved data. 
```
- time: 2 min, 17sek
- moved data: 16.95
- rotated data: 88.11
- test data: 98.26


## Experement 4
```

vi änrar modellen till convolutional model för se om det kan förbättra helheten. för att göra det mer intressant jag ändrar antalet neuroner till 28. då jag har strides till 8,8 och strides 1,1

Resutltatet var bra för moved data men inte för resten.
```
- time: 4 min, 31sek
- moved data: 19.14
- rotated data: 78.18
- test data: 97.81

## Experement 5
```

jag sänker antalet neuroner till 16 för att förbättra tiden då jag behåller antalet lager.  jag sätter strides till 12,12 för att förbättra resultatet och strides 1,1 och lr 0.5

Resultatet var bra för hela nästan mycket bättre än experment 3 om tiden inte inte var nästan 4 minuter.
```
- time: 3 min, 58sek
- moved data: 20.86
- rotated data: 88.59
- test data: 98.52


