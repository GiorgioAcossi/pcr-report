import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import io
import re
import zipfile
import time

# Funzione per rimuovere caratteri non validi dai nomi file
def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "-", filename)

# Funzione per generare il grafico a barre
def generate_bar_chart(labels_group1, values_group1, labels_group2, values_group2, title):
    x_group1 = np.arange(len(labels_group1))
    x_group2 = np.arange(len(labels_group2)) + len(labels_group1) + 2  # Crea uno spazio vuoto tra i gruppi

    # Combina le posizioni e le etichette
    x_positions = np.concatenate([x_group1, x_group2])
    all_labels = np.concatenate([labels_group1, labels_group2])

    # Crea il grafico con dimensioni più grandi
    fig, ax = plt.subplots(figsize=(12, 6))

    # Stili personalizzati e colori per ogni barra
    colors = ['black', 'white', 'gray', 'white', 'black', 'white', 'gray', 'white']
    hatches = ['', '', '', '//', '', '', '', '//']

    # Troncamento dei valori superiori a 2 e creazione delle barre
    truncated_values = np.concatenate([values_group1, values_group2])
    truncated_values = np.clip(truncated_values, 0, 2)  # Limita i valori a 2

    # Crea le barre con i bordi e le righe diagonali (hatching)
    bars = ax.bar(x_positions, truncated_values, color=colors, edgecolor='black')

    # Applica i pattern sulle barre
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    # Aggiungi un segno sopra le barre troncate
    for i, value in enumerate(np.concatenate([values_group1, values_group2])):
        if value > 2:
            ax.text(x_positions[i], 2, "↑", ha='center', va='bottom', fontsize=12, color='red')

    # Imposta il titolo del grafico
    ax.set_title(title)

    # Setta i limiti dell'asse Y e imposta l'intervallo massimo a 2
    ax.set_ylim(0, 2)

    # Imposta le etichette dell'asse X
    ax.set_xticks(x_positions)
    ax.set_xticklabels(all_labels)

    # Rimuovi i tick verticali sotto le barre
    ax.tick_params(axis='x', which='both', bottom=False)

    # Imposta le etichette orizzontali
    plt.xticks(rotation=0, ha="center")

    # Rimuovi solo i bordi superiori e destri, mantenendo visibili ascisse e ordinate
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Aggiusta il layout
    plt.tight_layout()

    return fig

# Funzione per caricare i dati dall'Excel
def load_data_from_excel(file):
    df = pd.read_excel(file)

    charts_data = []
    for i, row in df.iterrows():
        chart_name = row['Unnamed: 0']
        labels_group1 = df.columns[1:5]  # Colonne del primo gruppo
        values_group1 = row.iloc[1:5].tolist()  # Valori del primo gruppo
        labels_group2 = df.columns[5:]  # Colonne del secondo gruppo
        values_group2 = row.iloc[5:].tolist()  # Valori del secondo gruppo

        charts_data.append({
            'chart_name': chart_name,
            'labels_group1': labels_group1,
            'values_group1': values_group1,
            'labels_group2': labels_group2,
            'values_group2': values_group2
        })
    return charts_data

# Funzione per generare un archivio zip con i grafici
def generate_zip_with_charts(charts_data):
    # Creiamo un buffer di memoria per il file zip
    zip_buffer = io.BytesIO()

    # Creiamo un archivio zip
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for chart_data in charts_data:
            labels_group1 = chart_data['labels_group1']
            values_group1 = chart_data['values_group1']
            labels_group2 = chart_data['labels_group2']
            values_group2 = chart_data['values_group2']
            chart_name = chart_data['chart_name']

            title = f"{chart_name}"
            fig = generate_bar_chart(labels_group1, values_group1, labels_group2, values_group2, title)

            # Salva il grafico in un buffer di memoria
            chart_buffer = io.BytesIO()
            fig.savefig(chart_buffer, format="png")
            chart_buffer.seek(0)

            # Aggiungiamo il grafico come file png all'archivio zip
            zip_file.writestr(f"{clean_filename(chart_name)}.png", chart_buffer.getvalue())

    zip_buffer.seek(0)
    return zip_buffer

# Funzione per mostrare un messaggio temporaneo
def show_temporary_message(message, duration=1, message_type="success"):
    placeholder = st.empty()
    if message_type == "success":
        placeholder.success(message)
    elif message_type == "warning":
        placeholder.warning(message)
    elif message_type == "info":
        placeholder.info(message)
    elif message_type == "error":
        placeholder.error(message)
    # Attendi il tempo specificato e poi cancella il messaggio
    time.sleep(duration)
    placeholder.empty()

# Funzione per validare il contenuto del file Excel
def validate_excel_columns(df, required_columns):
    # Controlla se tutte le colonne richieste sono presenti nel DataFrame
    return all(column in df.columns for column in required_columns)

def main():
    st.title("PCR Report")

    # Colonne richieste per l'analisi (basate sul file caricato)
    required_columns = ['Unnamed: 0', 'P+FGF P1 N.', 'P+FGF P1 I.', 'P+PL P1 N.', 'P+PL P1 I.',
                        'P+FGF P3 N.', 'P+FGF P3 I.', 'P+PL P3 N.', 'P+PL P3 I.']

    # Carica il file Excel
    uploaded_file = st.file_uploader("Carica un file Excel", type=["xlsx"])

    if uploaded_file is not None:
        # Carica i dati dall'Excel
        df = pd.read_excel(uploaded_file)

        # Valida che le colonne richieste siano presenti
        if validate_excel_columns(df, required_columns):
            show_temporary_message("File caricato con successo!", duration=3, message_type="success")
            show_temporary_message("Analisi dei dati in corso...", duration=2, message_type="info")

            # Esegui l'analisi dei dati
            charts_data = load_data_from_excel(uploaded_file)

            show_temporary_message("File analizzato con successo!", duration=3, message_type="success")

            # Mostra i grafici solo se ci sono dati validi
            if charts_data:
                st.subheader("Grafici generati")

                # Genera il file zip con tutti i grafici
                zip_buffer = generate_zip_with_charts(charts_data)

                # Bottone per scaricare tutti i grafici in un file zip
                st.download_button(
                    label="Scarica tutti i grafici",
                    data=zip_buffer,
                    file_name="grafici.zip",
                    mime="application/zip"
                )

                # Mostra ogni grafico nella pagina
                for chart_data in charts_data:
                    labels_group1 = chart_data['labels_group1']
                    values_group1 = chart_data['values_group1']
                    labels_group2 = chart_data['labels_group2']
                    values_group2 = chart_data['values_group2']
                    chart_name = chart_data['chart_name']

                    title = f"{chart_name}"
                    fig = generate_bar_chart(labels_group1, values_group1, labels_group2, values_group2, title)

                    # Visualizza il grafico nell'interfaccia
                    st.pyplot(fig)
        else:
            show_temporary_message("Errore: Il file Excel non contiene le colonne richieste.", duration=5, message_type="error")


# Esegui l'app Streamlit
if __name__ == '__main__':
    main()
