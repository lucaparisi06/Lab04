class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = int(superficie)
        self.padiglione = int(padiglione)
        self.prezzo_base = float(prezzo_base)
        self.disponibile = True
        self.espositore = None

    def prezzo_finale(self):
        return self.prezzo_base

    def __eq__(self, other):
        if not isinstance(other, Stand):
            return False
        return self.codice == other.codice

    def __lt__(self, other):
        return self.prezzo_finale() < other.prezzo_finale()

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Non disponibile"
        return (
            f"{self.codice}: Standard | {self.superficie} mq - "
            f"Padiglione {self.padiglione} - "
            f"Prezzo {self.prezzo_finale():.2f}€ - {stato}"
        )


class StandPreseExtra(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, prese_extra):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.prese_extra = int(prese_extra)

    def prezzo_finale(self):
        return self.prezzo_base * (1 + 0.07 * self.prese_extra)

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Non disponibile"
        return (
            f"{self.codice}: Prese Extra | {self.superficie} mq - "
            f"Padiglione {self.padiglione} - "
            f"Prezzo {self.prezzo_finale():.2f}€ - "
            f"Prese aggiuntive: {self.prese_extra} - {stato}"
        )


class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def prezzo_finale(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Non disponibile"
        return (
            f"{self.codice}: Premium | {self.superficie} mq - "
            f"Padiglione {self.padiglione} - "
            f"Prezzo {self.prezzo_finale():.2f}€ - "
            f"Posizione: {self.posizione} - {stato}"
        )


class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand = None

    def __eq__(self, other):
        if not isinstance(other, Espositore):
            return False
        return self.codice == other.codice

    def __str__(self):
        if self.stand is None:
            return (
                f"{self.codice}: {self.nome} {self.cognome} - "
                "Nessuno stand assegnato"
            )

        return (
            f"{self.codice}: {self.nome} {self.cognome} - "
            f"Stand assegnato: {self.stand.codice}"
        )


class LingottoFiere:
    def __init__(self, nome):
        self.nome = nome
        self.stand = {}
        self.espositori = {}

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nuovo_nome):
        self._nome = nuovo_nome

    def carica_file_dati(self, file_path):
        self.stand = {}
        self.espositori = {}

        with open(file_path, "r", encoding="utf-8") as file:
            for riga in file:
                riga = riga.strip()

                if riga == "":
                    continue

                campi = riga.split(",")
                codice = campi[0].strip()

                if codice.startswith("ST"):
                    superficie = int(campi[1])
                    padiglione = int(campi[2])
                    prezzo_base = float(campi[3])

                    if len(campi) == 4:
                        stand = Stand(
                            codice, superficie, padiglione, prezzo_base
                        )
                    elif campi[4].strip().isdigit():
                        stand = StandPreseExtra(
                            codice, superficie, padiglione,
                            prezzo_base, campi[4]
                        )
                    else:
                        stand = StandPremium(
                            codice, superficie, padiglione,
                            prezzo_base, campi[4].strip()
                        )

                    self.stand[codice] = stand

                elif codice.startswith("ES"):
                    espositore = Espositore(
                        codice, campi[1].strip(), campi[2].strip()
                    )
                    self.espositori[codice] = espositore

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        if codice_stand not in self.stand:
            raise ValueError("Stand inesistente.")

        if codice_espositore not in self.espositori:
            raise ValueError("Espositore inesistente.")

        stand = self.stand[codice_stand]
        espositore = self.espositori[codice_espositore]

        if not stand.disponibile:
            raise ValueError("Lo stand non è disponibile.")

        if espositore.stand is not None:
            raise ValueError("L'espositore ha già uno stand assegnato.")

        stand.espositore = espositore
        stand.disponibile = False
        espositore.stand = stand

    def elenca_espositori(self):
        for codice in sorted(self.espositori):
            print(self.espositori[codice])

    def stand_ordinati_per_prezzo(self):
        return sorted(self.stand.values())


