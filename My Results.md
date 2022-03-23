

## Table of Frågor
- [A](#qa)

## Q(a)
```
Går det snabbare att träna nätverken (i antalet epoker) om vi ökar inlärningshastigheten (lr) på nätverken?
Kan vi ha en för stor inlärningshastighet och vad händer då?
```
## A(a)
```
Med en snabb inlärningstakt är det lättare att träna upp nätverken, men det finns risk att ta för många enorma steg, vilket minskar noggrannheten. Som ett resultat tar det längre tid att få en lika exakt modell.

lr 0,02, lr 0,7 och lr 1 jämförs.
Det tog längre tid för en modell med en inlärningshastighet på 0,02 att uppnå en hög noggrannhet till en början, och den var aldrig så exakt som de med 0,7 och 1 på 100 epoker. (figur 1)

Den roterade datan följde kurvan i figur 1, dock gjorde inte den förflyttade datan det.
```
![figur 1](/img/fig1.svg)


      
