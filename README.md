# School Project 2026 - Progetto Python AI Tris

## Descrizione

Questo progetto è stato sviluppato in Python e utilizza diverse librerie per la gestione delle funzionalità applicative, dell'interfaccia grafica e dell'interazione con il sistema operativo.

Perché il progetto funzioni è necessario avere un ambiente con le librerie richieste nei requisiti.

---

## Requisiti

Per eseguire il progetto è necessario avere installato:

- Python 3.11.0 (questa è la versione in cui è stato sviluppato, potrebbe non funzionare su versioni precedenti)

Python può essere scaricato dal sito ufficiale:

https://www.python.org/downloads/

Durante l'installazione si consiglia di selezionare l'opzione:

**Add Python to PATH**

per rendere disponibile il comando Python da qualsiasi terminale.

---

## Librerie utilizzate

### Librerie esterne

- pygame
- keyboard

### Librerie standard di Python

- random
- json
- os
- sys

Le librerie standard sono già incluse in Python e non richiedono installazioni aggiuntive.

---

## Installazione delle dipendenze

Qualora si desideri installare manualmente le librerie necessarie, eseguire il seguente comando da Prompt dei comandi o Terminale:

```bash
pip install pygame keyboard
```

In alternativa:

```bash
pip install pygame
pip install keyboard
```

---

## Avvio del progetto

Aprire un Prompt dei comandi nella cartella del progetto ed eseguire:

```bash
python nome_del_file_da_eseguire.py
```

I file `training1.py` e `training2.py` servono per costruire la qtable necessaria per far funzionare il gioco. Le qtable sono già costruite all'avvio, ma si possono ulteriormente addestrare o rifare da capo. Il file `play.py` avvia l'effettivo gioco.

---

## Struttura della soluzione

```text
school-rpject-2026-2/
├── play.py                     # Il gioco principale
├── training1.py                # Uno dei modi per trainare la qtable
├── training2.py                # Uno dei modi per trainare la qtable
├── utils.py                    # Libreria fatta da me
└── qtables/
    └── many qtables (as many as created)
```

---

## Note

Il progetto è un gioco di tris che l'utente gioca contro un'AI semplice fatta con la qtable. Ci sono due metodi per fare il training, quasi uguali. Viene creata una qtable per ogni bot con nome diverso.
All'interno del file `utils.py` sono presenti tutte le impostazioni riguardanti l'apprendimento.
