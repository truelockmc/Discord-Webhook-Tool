import time
import os
import logging
import requests
import random
import pystyle
import base64

# Löscht den Terminalbildschirm
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Holt JSON-Daten von der Webhook-URL, falls der Status 200 ist
def get_webhook_json(url):
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

# Fragt den Benutzer nach einer Eingabe und gibt diese zurück
def prompt_user(message):
    return input(f"{message} > ")

# Zeigt das Menü mit farbigem (Regenbogen-) Text an
def print_menu():
    options = ["Spam", "Delete", "Change Name", "One Message", "Check Status", "Exit"]
    for i, option in enumerate(options, 1):
        pystyle.Write.Print(f"\n[{i}] {option}", pystyle.Colors.rainbow)

# Function to send messages to the webhook
def spam_webhook(url, content):
    while True:
        try:
            # Send the message to the webhook
            response = requests.post(url, json={'content': content}, headers={'Content-Type': 'application/json'})
            
            if response.status_code == 204:
                # Successfully sent message in rainbow colors
                print(f"Successfully sent spam")
            elif response.status_code == 429:  # Rate limit reached
                reset_time = int(response.headers.get('X-RateLimit-Reset', 1))  # Time until reset in seconds
                pystyle.Write.Print(f"Rate limit reached. Waiting for {reset_time} seconds.", pystyle.Colors.rainbow)
                time.sleep(reset_time)  # Wait until the rate limit resets
            else:
                pystyle.Write.Print(f"Error whilst trying to send message: {response.status_code}", pystyle.Colors.rainbow)
        
        except requests.exceptions.RequestException as e:
            pystyle.Write.Print(f"An error occurred: {e}", pystyle.Colors.rainbow)
        
        # Decrease the wait time between messages
        time.sleep(random.uniform(0.1, 0.3))  # Wait time between 0.1 and 0.3 seconds
        
# Löscht den Webhook
def delete_webhook(url):
    response = requests.delete(url)
    if response.status_code == 204:
        print_delete_success()

# Ändert den Namen des Webhooks
def change_webhook_name(url, new_name):
    response = requests.patch(url, json={"name": new_name}, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print_change_name_success()
    else:
        logging.error(f"Failed to Change Name. Status Code: {response.status_code}")

# Sendet eine einmalige Nachricht an den Webhook
def send_one_time_message(url, content):
    response = requests.post(url, json={'content': content}, headers={'Content-Type': 'application/json'})
    if response.status_code == 204:
        print_one_time_message_success()

# Überprüft, ob der Webhook aktiv ist
def check_webhook_status(url):
    response = requests.get(url)
    if response.status_code == 200:
        print_status_success()
    else:
        if response.status_code == 404:
            logging.warning("Webhook Not Found.")
        else:
            logging.warning(f"Unknown Error Occurred. Status Code: {response.status_code}")

# Erfolgsmeldungen
def print_success_message():
    pystyle.Write.Print("Successfully sent message.", pystyle.Colors.rainbow)

def print_delete_success():
    pystyle.Write.Print("Successfully deleted.", pystyle.Colors.rainbow)

def print_change_name_success():
    pystyle.Write.Print("Successfully changed name.", pystyle.Colors.rainbow)

def print_one_time_message_success():
    pystyle.Write.Print("Successfully sent one-time message.", pystyle.Colors.rainbow)

def print_status_success():
    pystyle.Write.Print("Webhook is active.", pystyle.Colors.rainbow)

# Druckt die Signatur, die im Code base64-kodiert hinterlegt ist
def print_signature():
    # Base64-kodierter String: "Made - by Cxrve"
    signature = base64.b64decode("TWFkZSAtIGJ5IHRydWVfbG9jaw==").decode('utf-8')
    pystyle.Write.Print(signature, pystyle.Colors.rainbow)

# Initialisiert die Webhook-Interaktion und das Menü
def initialize_webhook():
    clear_terminal()
    print_signature()
    webhook_url = prompt_user("\nEnter Webhook URL")
    logging.info(f"Webhook URL Entered: {webhook_url}")
    webhook_data = get_webhook_json(webhook_url)
    if webhook_data:
        logging.info(f"Webhook Name Retrieved: {webhook_data['name']}")
    while True:
        clear_terminal()
        print_signature()
        print_menu()
        try:
            choice = int(prompt_user("\n>>> "))
        except ValueError:
            logging.error("Invalid input. Please enter a number.")
            time.sleep(2)
            continue

        if choice not in range(1, 7):
            logging.error("Invalid Choice Made. Please Try Again.")
            time.sleep(2)
            continue

        if choice == 1:
            content = prompt_user("Content")
            spam_webhook(webhook_url, content)
        elif choice == 2:
            delete_webhook(webhook_url)
        elif choice == 3:
            new_name = prompt_user("Name")
            change_webhook_name(webhook_url, new_name)
        elif choice == 4:
            content = prompt_user("Content")
            send_one_time_message(webhook_url, content)
        elif choice == 5:
            check_webhook_status(webhook_url)
        elif choice == 6:
            break

        time.sleep(random.uniform(0.5, 1.5))

if __name__ == "__main__":
    initialize_webhook()
