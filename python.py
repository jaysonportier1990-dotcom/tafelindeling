import tkinter as tk
from tkinter import messagebox


class TafelIndeler:
    def __init__(self, root):
        self.root = root
        self.root.title("Tafelindeler")
        self.root.geometry("900x600")

        self.tafels = {}
        self.personen = []

        # -------------------------
        # Linkerkant: personen
        # -------------------------
        links = tk.Frame(root, padx=10, pady=10)
        links.pack(side="left", fill="y")

        tk.Label(
            links,
            text="Personen",
            font=("Arial", 16, "bold")
        ).pack()

        self.persoon_entry = tk.Entry(links, width=25)
        self.persoon_entry.pack(pady=5)

        tk.Button(
            links,
            text="Persoon toevoegen",
            command=self.voeg_persoon_toe
        ).pack(pady=5)

        self.personen_lijst = tk.Listbox(links, width=25, height=25)
        self.personen_lijst.pack(pady=10)

        tk.Button(
            links,
            text="Persoon aan geselecteerde tafel zetten",
            command=self.zet_persoon_aan_tafel
        ).pack(pady=5)

        # -------------------------
        # Midden: tafels
        # -------------------------
        midden = tk.Frame(root, padx=10, pady=10)
        midden.pack(side="left", fill="both", expand=True)

        tk.Label(
            midden,
            text="Tafels",
            font=("Arial", 16, "bold")
        ).pack()

        tafel_frame = tk.Frame(midden)
        tafel_frame.pack(pady=10)

        self.tafel_naam_entry = tk.Entry(tafel_frame, width=15)
        self.tafel_naam_entry.pack(side="left")

        self.tafel_grootte_entry = tk.Entry(tafel_frame, width=8)
        self.tafel_grootte_entry.insert(0, "6")
        self.tafel_grootte_entry.pack(side="left", padx=5)

        tk.Button(
            tafel_frame,
            text="Tafel toevoegen",
            command=self.voeg_tafel_toe
        ).pack(side="left")

        self.tafels_frame = tk.Frame(midden)
        self.tafels_frame.pack(fill="both", expand=True)

        # -------------------------
        # Onderkant
        # -------------------------
        tk.Button(
            root,
            text="Willekeurig indelen",
            command=self.willekeurig_indelen
        ).pack(side="bottom", pady=10)

        tk.Button(
            root,
            text="Alles leegmaken",
            command=self.leegmaken
        ).pack(side="bottom", pady=5)

    def voeg_persoon_toe(self):
        naam = self.persoon_entry.get().strip()

        if not naam:
            messagebox.showwarning("Fout", "Vul eerst een naam in.")
            return

        if naam in self.personen:
            messagebox.showwarning("Fout", "Deze persoon bestaat al.")
            return

        self.personen.append(naam)
        self.personen_lijst.insert(tk.END, naam)
        self.persoon_entry.delete(0, tk.END)

    def voeg_tafel_toe(self):
        naam = self.tafel_naam_entry.get().strip()

        try:
            grootte = int(self.tafel_grootte_entry.get())
        except ValueError:
            messagebox.showwarning(
                "Fout",
                "De grootte van de tafel moet een getal zijn."
            )
            return

        if not naam:
            messagebox.showwarning("Fout", "Geef de tafel een naam.")
            return

        if grootte <= 0:
            messagebox.showwarning(
                "Fout",
                "Een tafel moet minimaal 1 plek hebben."
            )
            return

        if naam in self.tafels:
            messagebox.showwarning("Fout", "Deze tafel bestaat al.")
            return

        self.tafels[naam] = {
            "grootte": grootte,
            "personen": []
        }

        self.tafel_naam_entry.delete(0, tk.END)
        self.tafels_opnieuw_tekenen()

    def zet_persoon_aan_tafel(self):
        selectie = self.personen_lijst.curselection()

        if not selectie:
            messagebox.showwarning(
                "Fout",
                "Selecteer eerst een persoon."
            )
            return

        if not self.tafels:
            messagebox.showwarning(
                "Fout",
                "Voeg eerst een tafel toe."
            )
            return

        persoon = self.personen[selectie[0]]

        # Persoon eventueel van een andere tafel verwijderen
        for tafel in self.tafels.values():
            if persoon in tafel["personen"]:
                tafel["personen"].remove(persoon)

        # Vraag aan welke tafel de persoon moet
        keuze = TafelKeuze(self.root, list(self.tafels.keys()))

        self.root.wait_window(keuze.venster)

        if keuze.resultaat is None:
            return

        tafelnaam = keuze.resultaat
        tafel = self.tafels[tafelnaam]

        if len(tafel["personen"]) >= tafel["grootte"]:
            messagebox.showwarning(
                "Tafel vol",
                f"{tafelnaam} heeft geen vrije plaatsen meer."
            )
            return

        tafel["personen"].append(persoon)
        self.tafels_opnieuw_tekenen()

    def tafels_opnieuw_tekenen(self):
        for widget in self.tafels_frame.winfo_children():
            widget.destroy()

        for naam, tafel in self.tafels.items():
            frame = tk.LabelFrame(
                self.tafels_frame,
                text=f"{naam} ({len(tafel['personen'])}/{tafel['grootte']})",
                padx=10,
                pady=10
            )

            frame.pack(fill="x", pady=5)

            if tafel["personen"]:
                for persoon in tafel["personen"]:
                    tk.Label(
                        frame,
                        text="• " + persoon,
                        anchor="w"
                    ).pack(fill="x")
            else:
                tk.Label(
                    frame,
                    text="Nog niemand aan deze tafel"
                ).pack()

    def willekeurig_indelen(self):
        import random

        if not self.tafels:
            messagebox.showwarning(
                "Fout",
                "Voeg eerst tafels toe."
            )
            return

        personen = self.personen.copy()
        random.shuffle(personen)

        # Alle tafels leegmaken
        for tafel in self.tafels.values():
            tafel["personen"].clear()

        overgebleven = []

        for persoon in personen:
            geplaatst = False

            tafels = list(self.tafels.values())
            random.shuffle(tafels)

            for tafel in tafels:
                if len(tafel["personen"]) < tafel["grootte"]:
                    tafel["personen"].append(persoon)
                    geplaatst = True
                    break

            if not geplaatst:
                overgebleven.append(persoon)

        self.tafels_opnieuw_tekenen()

        if overgebleven:
            messagebox.showinfo(
                "Niet genoeg plaatsen",
                "Deze personen konden niet worden geplaatst:\n\n"
                + "\n".join(overgebleven)
            )

    def leegmaken(self):
        for tafel in self.tafels.values():
            tafel["personen"].clear()

        self.tafels_opnieuw_tekenen()


class TafelKeuze:
    def __init__(self, root, tafels):
        self.resultaat = None

        self.venster = tk.Toplevel(root)
        self.venster.title("Kies een tafel")
        self.venster.geometry("300x300")

        tk.Label(
            self.venster,
            text="Aan welke tafel?",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        for tafel in tafels:
            tk.Button(
                self.venster,
                text=tafel,
                width=20,
                command=lambda t=tafel: self.kies(t)
            ).pack(pady=3)

    def kies(self, tafel):
        self.resultaat = tafel
        self.venster.destroy()


# Programma starten
root = tk.Tk()
app = TafelIndeler(root)
root.mainloop()