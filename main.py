"""SmartWeather: interface Tkinter para consulta automatizada do clima."""
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import database
from weather import get_weather, recommend


class SmartWeather(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartWeather | Assistente de Clima")
        self.geometry("780x570")
        self.minsize(650, 480)
        self.configure(bg="#101827")
        self.city = tk.StringVar(value="São Paulo")
        database.initialize()
        self.build_ui()
        self.refresh_history()

    def build_ui(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=27)
        tk.Label(self, text="☁ SmartWeather", font=("Segoe UI", 25, "bold"),
                 bg="#101827", fg="#f4f7ff").pack(pady=(22, 4))
        tk.Label(self, text="Clima atual, recomendações e histórico em um só lugar",
                 bg="#101827", fg="#a8bbd4", font=("Segoe UI", 11)).pack()
        bar = tk.Frame(self, bg="#101827")
        bar.pack(fill="x", padx=32, pady=20)
        tk.Entry(bar, textvariable=self.city, font=("Segoe UI", 13), width=35).pack(side="left", fill="x", expand=True, ipady=6)
        self.search_btn = tk.Button(bar, text="Consultar clima", command=self.search,
                                    bg="#2f81f7", fg="white", font=("Segoe UI", 11, "bold"))
        self.search_btn.pack(side="left", padx=(10, 0), ipadx=8, ipady=4)
        self.result = tk.Label(self, text="Digite uma cidade e clique em Consultar clima.",
                               font=("Segoe UI", 12), bg="#172438", fg="white",
                               justify="left", anchor="nw", padx=20, pady=16, wraplength=690)
        self.result.pack(fill="x", padx=32)
        tk.Label(self, text="Últimas consultas", bg="#101827", fg="white",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=32, pady=(20, 8))
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=32)
        columns = ("data", "cidade", "temp", "chuva")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=7)
        for col, title, width in zip(columns, ("Consulta (UTC)", "Cidade", "Temp. °C", "Chuva mm"), (180, 180, 100, 100)):
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor="center")
        self.table.pack(fill="both", expand=True)
        tk.Button(self, text="Exportar histórico em CSV", command=self.export,
                  bg="#263951", fg="white", font=("Segoe UI", 11)).pack(pady=16, ipadx=12, ipady=5)

    def search(self):
        city = self.city.get()
        self.search_btn.config(state="disabled")
        self.result.config(text="Consultando a API, aguarde...")
        threading.Thread(target=self.worker, args=(city,), daemon=True).start()

    def worker(self, city):
        try:
            data = get_weather(city)
            database.save(data)
            self.after(0, lambda: self.show_weather(data))
        except Exception as exc:
            error_message = str(exc)
            self.after(0, lambda: self.show_error(error_message))

    def show_weather(self, data):
        tips = "\n".join("• " + tip for tip in recommend(data))
        self.result.config(text=(
            f"{data['cidade']} — {data['pais']} | {data['horario']}\n"
            f"Temperatura: {data['temperatura']} °C   |   Sensação: {data['sensacao']} °C\n"
            f"Umidade: {data['umidade']}%   |   Precipitação atual: {data['precipitacao']} mm\n"
            f"Vento: {data['vento']} km/h\n\nRecomendações:\n{tips}"))
        self.search_btn.config(state="normal")
        self.refresh_history()

    def show_error(self, error):
        self.result.config(text="Erro: " + error)
        self.search_btn.config(state="normal")

    def refresh_history(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for row in database.recent():
            self.table.insert("", "end", values=(row[0], row[1], row[3], row[6]))

    def export(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")],
                                            initialfile="smartweather_historico.csv")
        if path:
            try:
                database.export_csv(path)
                messagebox.showinfo("Sucesso", "Histórico exportado com sucesso!")
            except OSError as exc:
                messagebox.showerror("Erro", str(exc))


if __name__ == "__main__":
    SmartWeather().mainloop()
