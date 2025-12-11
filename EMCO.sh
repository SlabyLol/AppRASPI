#!/bin/bash
# Kombiniertes Notfall-Tool für Raspberry Pi
# Nur für Tobias & Simon

# Prüfen, ob zenity installiert ist
if ! command -v zenity &> /dev/null
then
    echo "Zenity ist nicht installiert. Installiere es mit: sudo apt install zenity -y"
    exit
fi

# Hauptmenü
aktion=$(zenity --list --title="Notfall-Station" \
--text="Wähle die gewünschte Aktion:" \
--column="Aktion" "Abmelden" "Neustart" "Abbrechen")

case $aktion in
    "Abmelden")
        zenity --question --title="Abmelden" --text="Willst du die aktuelle Sitzung sofort abmelden?" --ok-label="Ja" --cancel-label="Nein"
        if [ $? = 0 ]; then
            logout
            exit
        fi
        ;;
    "Neustart")
        zenity --question --title="Neustart" --text="Willst du den Raspberry Pi sofort neu starten?" --ok-label="Ja" --cancel-label="Nein"
        if [ $? = 0 ]; then
            sudo reboot
        fi
        ;;
    "Abbrechen")
        exit
        ;;
esac
