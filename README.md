# bp-Heartbleed-attack-game
Repozitár obsahuje všetky potrebné súbory pre spustenie bezpečnostnej hry typu Capture the Flag (Attack-only) k bakalárskej práci Bezpečnosť protokolu SSL/TLS. Hra demonštruje závažnosť chyby Heartbleed. Virtuálne prostredie bude zahŕňať tri stroje - počítač útočníka (IP adresa 10.11.30.2), používateľa (IP adresa 10.11.30.4) a server (IP adresa 10.11.30.3). Stroje sú usporiadané podľa topológie v súbore **attack_topology.png** a vybavené operačnými systémemi Kali Linux a Ubuntu. Cieľový stroj disponuje zraniteľnou verziou knižnice OpenSSL 1.0.1.

![Topológia](https://github.com/dorota-fiit/bp-Heartbleed-attack-game/blob/main/attack_topology.png)

## Zraniteľnosť Heartbleed 
Heartbleed je implementačná chyba SSL/TLS heartbeat rozšírenia v rámci OpenSSL a umožňuje útočníkovi získavať dáta zo vzdialeného servera, pričom ukradnuté dáta môžu zahŕňať napríklad používateľské mená, heslá alebo platobné údaje. SSL/TLS protokol slúži na vytvorenie bezpečného komunikačného kanálu medzi aplikáciami. Kvôli výpočtovým postupom ako šifrovanie a dešifrovanie verejného kľúča alebo výmena kľúčov je vytvorenie nového kanálu pomerne nákladné. Aj napriek tomu, ak server a klient nekomunikujú, kanál medzi nimi sa po určitom čase preruší a spojenie musí byť pri ďalšej komunikácii opätovne nadviazané. S cieľom minimalizovať náklady bolo implementované riešenie prostredníctvom rozšírenia heartbeat.  Heartbeat poskytuje nový protokol implementujúci keep-alive funkcionalitu protokolu SSL/TLS.

Prvým krokom v rámci tejto funkcionality je odoslanie Heartbeat paketu, nazývaného žiadosť, príjemcovi. Po prijatí prijímateľ skonštruuje paket predstavujúci odpoveď a odošle ho odosielateľovi. Správa HeartbeatResponse by mala niesť obsah zhodný so žiadosťou a svoju vlastnú náhodnú výplň. Zraniteľnosť je spôsobená kódom, ktorý nesprávne validuje vstupy pri kopírovaní dát z privátnej pamäte do odchádzajúceho paketu. Obsah žiadosti sa kopíruje do paketu odpovede, no veľkosť kopírovaného obsahu nie je určená jeho reálnou veľkosťou, ale veľkosťou zadanou odosielateľom. memcpy() teda skopíruje viac dát do paketu odpovedi ako je v pakete žiadosti. Začne kopírovaním obsahu paketu žiadosti, no postupne prekročí hranicu obsahu a začne kopírovať aj dáta uchovávané v pamäti nad ním. Práve táto pamäť môže obsahovať senzitívne používateľské informácie. Získané informácie sa spolu s obsahom prekopírujú do paketu odpovede a sú odoslané v HeartbeatResponse útočníkovi. Útočníkovi to umožňuje čítať dáta uložené v privátnej pamäti, ktoré mohli potenciálne zahŕňať aj dáta prenášané bezpečným kanálom a kryptografické tajomstvá.
## Zadanie
Keďže ide o hru Attack-only, hráč má za úlohu získať vlajku zo zraniteľného servera. Vlajka je umiestnená v správe odoslanej v rámci automatizovanej interakcie používateľa na sociálnej sieti (https://www.heartbleedlabelgg.com). Hráč - útočník má 15 minút na oboznámenie sa s predpripraveným škodlivým kódom, na jeho úpravu a získanie všetkých potrebných dát z cieľového stroja. Po 15 minútach sa na cieľovom stroji aktualizuje knižnica OpenSSL na zabezpečenú verziu 1.0.1g, zablokuje sa IP adresa útočníka a útočník nebude môcť ukradnúť žiadne ďalšie citlivé údaje používateľa. Vzhľadom na zložitosť riešenia bude mať hráč predpripravený škodlivý kód (**attack.py**) v priečinku **/home/kali/**. Jeho preštudovaním by mal získať všetky potrebné informácie k odoslaniu Heartbeat paketu na zraniteľný server. Po jeho odoslaní je potrebné sledovať informácie a obsah odpovede priamo v termináli. Pred nastavením prostredia a inštaláciou si odporúčam prečítať vopred celý návod. Riešenie obsahuje všetky kroky potrebné na úspešne získanie vlajky. 
## Prostredie a inštalácia
Hra je spustiteľná v prostredí nástroja KYPO Cyber Sandbox Creator. Pri inštalácii nástroja prosím postupujte podľa nasledujúceho návodu -  https://gitlab.ics.muni.cz/muni-kypo-csc/cyber-sandbox-creator/-/wikis/3.0/Installation. 

Po nainštalovaní prostredia si stiahnite repozitár do Vášho počítača. Obsah vlajky je prednastavený na hodnotu "Insert body of the flag here." a pred vytváraním strojov je možné ho zmeniť podľa Vašich požiadaviek v súbore **muni-kypo_vms/user/interaction3.py**. Následne  vytvoríme virtuálne stroje - počítač útočníka (Vy) a používateľa. V termináli prejdite do priečinku **muni-kypo_vms** a zadajte príkaz `create-sandbox --provisioning-dir .\provisioning attack_topology.yml`, ktorý vytvorí prechodnú definíciu sandboxu (priečinok **sandbox**). Následne prejdite do priečinku **sandbox** a zadajte príkaz na vytvorenie virtuálnych strojov - `manage-sandbox build`. Vo VirtualBoxe sa postupne vytvoria stroje: router, attacker a user. Dôležité je vytvoriť aj server. Nakoniec v termináli prejdite do priečinku **vagrant_server** a zadajte príkaz `vagrant up`. Týmto príkazom sa Vám vo VirtualBoxe vytvorí virtuálny stroj servera. Pozor! Stroj sa po vytvorení nepripojí do požadovanej siete a pre to je ho nutné reštartovať. Vo VirtualBox okne virtuálneho stroja kliknite v menu na "Machine" a vyberte možnosť "Reset". Stroj musí byť reštartovaný IHNEĎ po vytvorení, keďže sú zapnuté časovače na hru a zabezpečenie. 
## Riešenie
1. Do počítača útočníka sa prihláste pomocou mena "kali" a hesla "kali".
2. Zapnite terminál a prejdite do priečinka **home/kali**.\
`cd /home/kali`
3. Otvorte súbor **attack.py** a nájdite príkaz na odoslanie žiadosti `HeartbeatRequest` na zraniteľný server. Skúste žiadosť odoslať.

    <details><summary>Nápoveda</summary>
        ./attack.py www.heartbleedlabelgg.com
    </details>

4. Odoslanie neprebehne keďže súbor nie je vykonateľný. Zmeňte teda súbor **attack.py** na vykonateľný. 
  
    <details><summary>Nápoveda</summary>
        sudo chmod +x attack.py
    </details>
  
5. Znova odošlite škodlivý kód v podobe `HeartbeatRequest` na zraniteľný server.
 
   <details><summary>Nápoveda</summary>
      ./attack.py www.heartbleedlabelgg.com
    </details>
  
6. V tomto momente vidíte v termináli vypísané informácie a obsah odpovede. Informácie obsahujú hlášku "Server processed malformed heartbeat, but did not return any extra data.". Na základe tohto zistenia je potrebné upraviť hodnotu zapísanú v poli veľkosti obsahu. Otvorte teda súbor **attack.py**, prejdite si znova kód, nájdite prepínač na zmenu dĺžky odpovede a jeho predvolenú hodnotu. 
 
   <details><summary>Nápoveda</summary>
      Prepínače na zmenu dĺžky odpovede sú -l alebo --length. Ich predvolená veľkosť je 0x16.
    </details>
  
7. Zmente dĺžku obsahu odpovede a skúste odoslať žiadosť na zraniteľný server. Odosielanie opakujte až kým nezískate osobné údaje používateľa (vrátane vlajky).

    <details><summary>Nápoveda</summary>
        Prvou možnosťou je zmena default hodnoty priamo v kóde. Druhou možnosťou je obmienanie dĺžky pomocou prepínačov "-l" a "--length" priamo v termináli. Skúste odoslať žiadosť na zraniteľný server napríklad príkazom "./attack.py www.heartbleedlabelgg.com -l 0x4000". 
      </details>
  
## Zdroje
https://web.ecs.syr.edu/~wedu/seed/Labs_12.04/Networking/Heartbleed/

