class Strumento:
    # alloca la memoria e assegna i valori agli attributi
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        """Inizializza un singolo strumento"""
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno_acquisto)
        self.valore = float(valore)

    def __str__(self):
        return f"[{self.codice}] {self.tipo} {self.marca} (Anno: {self.anno_acquisto}, Valore: {self.valore:.2f}€)"

    def __lt__(self, other):
        return self.marca < other.marca


class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        """Inizializza un singolo prestito"""
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"Prestito {self.id_prestito}: Strumento {self.id_strumento} a {self.cognome_allievo} (Data: {self.data})"


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self.nome = nome
        self.responsabile = responsabile
        # strutture dati nell'oggetto
        self.strumenti = []
        self.prestiti = []
        self.contatore_prestiti = 1

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        with open(file_path, "r") as f:
            for riga in f:
                dati = riga.strip().split(",")
                if len(dati) == 5:
                    # creazione di un oggetto con return di riferimento
                    nuovo_strumento = Strumento(dati[0], dati[1], dati[2], dati[3], dati[4])
                    self.strumenti.append(nuovo_strumento)

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        max_id = 0
        # iterazione sugli oggetti presenti in memoria
        for s in self.strumenti:
            num = int(s.codice.replace("S", ""))
            if num > max_id:
                max_id = num

        nuovo_codice = f"S{max_id + 1}"
        nuovo_strumento = Strumento(nuovo_codice, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(nuovo_strumento)
        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        # copia della lista per non alterare l'originale
        strumenti_ordinati = list(self.strumenti)
        strumenti_ordinati.sort()
        return strumenti_ordinati

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        trovato = False
        for s in self.strumenti:
            # attributi degli oggetti anziché l'identità
            if s.codice == id_strumento:
                trovato = True

        if not trovato:
            raise Exception("Errore: strumento non presente nel sistema.")

        for p in self.prestiti:
            if p.id_strumento == id_strumento:
                raise Exception("Errore: strumento attualmente già in prestito.")

        id_prestito = f"P{self.contatore_prestiti}"
        self.contatore_prestiti += 1

        # nuovo oggetto con la funzione __init__
        nuovo_prestito = Prestito(id_prestito, data, id_strumento, cognome_allievo)
        self.prestiti.append(nuovo_prestito)
        return nuovo_prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        da_rimuovere = None
        for p in self.prestiti:
            if p.id_prestito == id_prestito:
                da_rimuovere = p

        if da_rimuovere:
            self.prestiti.remove(da_rimuovere)
        else:
            raise Exception("Errore: prestito non trovato.")