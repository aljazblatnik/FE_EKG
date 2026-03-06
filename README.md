# Vzpostavitev razvojnega okolja in uporaba EKG ščita z Arduino Nano

Ta dokument vsebuje uradna navodila za pripravo in konfiguracijo razvojnega okolja Arduino IDE, vzpostavitev povezave s ploščami Arduino Nano ter nalaganje in zagon kode za branje EKG signala.

---

## 1. Prenos in namestitev Arduino IDE

Če razvojnega okolja Arduino IDE še nimate, ga namestite po naslednjem postopku:

1. Obiščite uradno spletno stran [arduino.cc/en/software](https://www.arduino.cc/en/software).
2. Prenesite najnovejšo različico programske opreme, ki ustreza vašemu operacijskemu sistemu (Windows, macOS ali Linux).
3. Zaženite preneseno namestitveno datoteko in sledite navodilom čarovnika za namestitev.

## 2. Namestitev gonilnikov za serijsko komunikacijo (CH340)

Večina neoriginalnih plošč (klonov) Arduino Nano za USB komunikacijo namesto originalnega čipa uporablja alternativno integrirano vezje CH340. Da operacijski sistem napravo prepozna in ji dodeli navidezna serijska vrata (COM port), je zahtevana namestitev ustreznih gonilnikov.

> **Opomba za uporabnike OS Windows:** Ob namestitvi okolja Arduino IDE se na sistem Windows 11 gonilniki namestijo samodejno! Uspešnost namestitve lahko preverite v *Upravitelju naprav (Device Manager)*. Pod zavihkom *Vrata (COM in LPT)* se mora nahajati naprava z imenom **USB-SERIAL CH340 (COMx)**.

## 3. Konfiguracija razvojnega okolja Arduino IDE

Po uspešni strojni povezavi je potrebno razvojnemu okolju določiti tip plošče in ustrezne parametre za nalaganje kode.

1. Odprite aplikacijo **Arduino IDE**.
2. V vrstici z meniji izberite **Tools (Orodja)** > **Board (Plošča)** > **Arduino AVR Boards** in kliknite na **Arduino Nano**.
3. Za izbiro komunikacijskih vrat pojdite na **Tools (Orodja)** > **Port (Vrata)** in izberite vrata (**COMx**), ki pripadajo CH340 napravi.

## 4. Preverjanje delovanja sistema (Test utripanja)

Pred nadaljevanjem je priporočljivo preveriti, ali je povezava uspešna.

1. V meniju izberite **File (Datoteka)** > **Examples (Primeri)** > **01.Basics** > **Blink**. 
2. V zgornjem levem kotu kliknite gumb **Upload (Naloži)** (ikona s puščico v desno).
3. Uspešen prenos potrjuje sporočilo **Done uploading** v konzoli na dnu zaslona. Na plošči Arduino bo začela utripati vgrajena LED dioda (označena s črko "L").

## 5. Nalaganje kode za EKG ščit

Ko je okolje uspešno nastavljeno, sledite spodnjim korakom za zagon EKG senzorja.

1. V Arduino IDE ustvarite nov projekt: **File (Datoteka)** > **New (Nova)**.
2. Izbrišite privzeto kodo in v prazno okno prilepite naslednjo programsko kodo:

```cpp
void setup() {
  // Inicializacija serijske komunikacije pri hitrosti 9600 baudov:
  Serial.begin(9600);
  
  // Nastavitev digitalnih pinov za zaznavanje odklopljenih elektrod (Leads Off):
  pinMode(9, INPUT);  // Nastavitev za detekcijo odklopa pozitivne elektrode (LO +)
  pinMode(10, INPUT); // Nastavitev za detekcijo odklopa negativne elektrode (LO -)
}

void loop() {
  // Branje analogne vrednosti iz EKG senzorja (pin A0) in 
  // pošiljanje prebranega vzorca na serijski port:
  Serial.println(analogRead(A0));
  
  // Kratka zakasnitev (1 milisekunda) med posameznimi meritvami,
  // ki preprečuje preobremenitev serijske komunikacije:
  delay(1);
}
```
## 6. Nameščanje elektrod
Na ustrezna mesta na telesu namestite tri elektrode. Pred priklopom na EKG se prepričajte, da je prenosni računalnik odklopljen iz napajalnika in ni povezan z nobeno drugo napravo!

## 7. Vzpostavitev Python okolja in zagon vizualizacije

Za prikaz in obdelavo EKG signala v realnem času na računalniku je priložena skripta v programskem jeziku Python. Izbirate lahko med programom, ki je že pripravljen za uporabo, ali pa sami poženete Python skripto. Če želite preskočiti korak za ustvarjanje lastne kode in želite zgolj preveriti delovanje, nadaljujte na korak 8. 

Da bi skripto lahko uspešno zagnali, je potrebno predhodno namestiti Python interpret in nekaj dodatnih knjižnic.

### Korak 7.1: Prenos in namestitev Pythona

Če Pythona na vašem sistemu še nimate nameščenega, sledite spodnjim korakom:

1. Obiščite uradno spletno stran [python.org/downloads](https://www.python.org/downloads/).
2. Prenesite najnovejši namestitveni paket za vaš operacijski sistem.
3. Zaženite namestitveno datoteko.
4. **Zelo pomembno (za uporabnike Windows):** Na prvem oknu namestitvenega programa obvezno obkljukajte možnost **"Add Python to PATH"** (ali *Add Python to environment variables*). Brez te nastavitve računalnik ne bo prepoznal ukazov za nameščanje dodatkov.
5. Kliknite **"Install Now"** in počakajte, da se namestitev zaključi.

### Korak 7.2: Namestitev potrebnih knjižnic

Python skripta za vizualizacijo EKG signala uporablja zunanje knjižnice za branje podatkov preko USB vrat in izrisovanje grafov. Te knjižnice namestimo s pomočjo orodja `pip` (Python Package Installer).

1. Odprite terminal oziroma ukazno vrstico:
   * **Windows:** Pritisnite tipko `Windows`, vpišite `cmd` in pritisnite `Enter` (Ukazni poziv).
   * **macOS / Linux:** Odprite aplikacijo `Terminal`.
2. V terminal vnesite naslednji ukaz in pritisnite `Enter`:

```bash
pip install pyserial matplotlib
```

3. Počakajte, da sistem prenese in namesti knjižnice. Namestitev je uspešna, ko terminal znova prikaže vnosno vrstico brez sporočil o napakah.

### Korak 7.3: Zagon vizualizacijske skripte

Ko sta strojna oprema (Arduino) in programska oprema (Python okolje) pripravljeni, lahko zaženete grafični vmesnik.

1. Prepričajte se, da je Arduino Nano priključen na računalnik in da je serijski monitor/risalnik v aplikaciji Arduino IDE zaprt. (Serijska vrata lahko hkrati uporablja samo en program!)
2. Prenesite Python datoteko (`Prikaz_EKG_python.py`) na vaš računalnik. 
3. V terminalu se s pomočjo ukaza `cd` pomaknite v mapo, kjer se nahaja datoteka (npr. `cd Desktop/Prikaz_EKG_python.py`)
4. Skripto zaženite z naslednjim ukazom:

```bash
python Prikaz_EKG_python.py
```

5. Če je vse uspešno nastavljeno, bo skripta samodejno poiskala ustrezna serijska vrata in odprla novo okno z animiranim grafom vašega srčnega utripa in izračunanim BPM (udarcem na minuto).

## 8. Uporaba predpripravljenega programa

Za uporabnike operacijskega sistema Windows, ki ne želijo nameščati programskega jezika Python in dodatnih knjižnic, je na voljo že prevedena, samostojna izvedljiva datoteka (`.exe`). Vsa potrebna programska oprema za vizualizacijo je že vgrajena v to datoteko.

> **⚠️ Ključno opozorilo:** Čeprav ne potrebujete nameščati Pythona, pa vaš računalnik za komunikacijo z Arduino Nano še vedno **nujno potrebuje strojni gonilnik za čip CH340**. Brez njega operacijski sistem naprave ne bo prepoznal in program ne bo deloval. Postopek namestitve gonilnika je opisan v poglavju 1.2 zgoraj.

### Navodila za uporabo:

1. **Prenos programa:** Prenesite datoteko `Prikaz_EKG_python.exe` iz razdelka *Releases* (Izdaje) v tem repozitoriju (oz. iz ponujene povezave).
2. **Priprava strojne opreme:** Prepričajte se, da ste uspešno namestili CH340 gonilnik.
3. **Povezava:** S priloženim USB kablom povežite Arduino Nano (z EKG ščitom) na vaš računalnik.
4. **Sprostitev vrat:** Prepričajte se, da imate na računalniku **zaprt** Arduino IDE (predvsem okna *Serial Monitor* ali *Serial Plotter*), saj lahko serijska vrata hkrati uporablja le en program.
5. **Zagon:** Dvokliknite na datoteko `Prikaz_EKG_python.exe`. 
   
Program bo samodejno preiskal vsa razpoložljiva USB/COM vrata, poiskal vaš Arduino in odprl novo okno z grafičnim izrisom vašega EKG signala in izračunanim srčnim utripom (BPM) v realnem času.

### Reševanje težav ob zagonu:
* **Program se odpre in takoj zapre:** To običajno pomeni, da program ni našel Arduina. Preverite, ali je USB kabel dobro priključen in ali je računalnik prepoznal napravo (v Upravitelju naprav preverite prisotnost *USB-SERIAL CH340*).
* **Opozorilo sistema Windows (SmartScreen):** Ker aplikacija morda nima komercialnega digitalnega potrdila, vas bo Windows Defender ob prvem zagonu morda opozoril. V tem primeru kliknite **"Več informacij" (More info)** in nato **"Vseeno zaženi" (Run anyway)**.

## 10. Pravilna namestitev elektrod na telo

Za zagotovitev najboljše meritve in čim manj šuma v signalu je ključna pravilna namestitev elektrod na telo. Priporočljivo je, da senzorje (samolepilne elektrode) najprej pripnete na kable in jih šele nato namestite na telo. Bližje kot so elektrode srcu, boljša in bolj natančna bo meritev.

Kabli imajo barvne oznake, ki so osnovane na Einthovnovem trikotniku, da vam pomagajo pri pravilni namestitvi:
* **RA - Right Arm:** Desna roka (podlaket) ali desna stran prsnega koša blizu roke.
* **LA - Left Arm:** Leva roka (podlaket) ali leva stran prsnega koša blizu roke.
* **RL - Right Leg:** Desna noga ali desni spodnji del trebuha (tik nad desnim bokom).

**Nasveti za izboljšanje kakovosti EKG signala:**
* Senzorje namestite čim bližje srcu (namestitev na prsni koš in trebuh je boljša od namestitve na okončine).
* Prepričajte se, da sta RA in LA elektroda na ustreznih, nasprotnih straneh srca.
* Med merjenjem bodite čim bolj pri miru, saj vsakršen premik mišic povzroči motnje v signalu.
* Za vsako meritev uporabite nove, sveže elektrode, saj lepilo z večkratno uporabo izgubi prevodnost.
* Območje kože, kamor boste prilepili elektrode, predhodno očistite, saj dlake ali maščoba na koži niso dober prevodnik.

---

## 11. Kako odčitavati in razumeti EKG

Elektrokardiogram (EKG) grafično prikazuje električno aktivnost vašega srca, ki jo lahko razdelimo na več ključnih intervalov. Ko so senzorji pravilno nameščeni in ste pri miru, bi morali videti jasno obliko valovanja.

Pri analizi EKG grafa ste pozorni na naslednje valove in intervale:
* **PR interval:** To je začetni val na grafu, ki ga ustvari električni impulz, ko potuje od desnega preddvora k levemu. Ta impulz povzroči depolarizacijo oziroma krčenje preddvorov, ki takrat potisneta kri naprej v prekata.
* **QRS kompleks (znotraj QT intervala):** To je glavni "utrip", ki ga vidimo kot izrazit, visok in oster vrh na EKG grafu, ter tisti del, ki ga srčni monitorji zaznavajo za klasični pisk. Med QRS kompleksom začneta močno črpati oba prekata; desni prekat črpa deoksigenirano kri v pljuča, levi pa potiska sveže oksigenirano kri skozi aorto po celem telesu.
* **ST segment:** Takoj po ostrem krčenju se graf umiri; ta segment je električno precej miren in predstavlja časovno okno, ko prekata mirujeta in čakata na ponovno repolarizacijo.
* **T val:** Na koncu utripa se pojavi manjši val, ki označuje repolarizacijo oziroma sprostitev prekatov, ko se srce pripravlja na nov cikel.