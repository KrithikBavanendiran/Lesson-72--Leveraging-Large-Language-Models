import requests
from config import HF_API_KEY
from colorama import Fore, Style, init

init(autoreset=True)

DEFAULT_MODEL = "facebook/bart-large-cnn"

def build_api_url(model_name):
    return f"https://router.huggingface.co/hf-inference/models/{model_name}"

def query(payload, model_name=DEFAULT_MODEL):
    """Send a POST request to the Hugging Face API using the specified model."""

    api_url= build_api_url(model_name)
    headers={"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}

    response = requests.post(api_url, headers=headers, json=payload)
    print(response.status_code)
    print(response.text) 
    
    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")
    return response.json()

def summarize(text, min_length, max_length, model_name=DEFAULT_MODEL):
    payload = {"inputs": text, "parameters": {"min_length": min_length, "max_length": max_length}}
    print(Fore.BLUE + Style.BRIGHT + f"Performing AI summarization using model: {model_name}")
    result = query(payload, model_name=model_name)
    if isinstance(result, list) and result and "summary_text" in result[0]:
        return result[0]["summary_text"]
    else:
        print(Fore.RED+"Error in summarization response: ", result)
        return None
    
if __name__ == "__main__":
    print(Fore.YELLOW + Style.BRIGHT + "Hi there! What's your name?")
    user_name = input("Enter your name: ").strip()
    if not user_name:
        user_name = "User"
    print(Fore.GREEN + Style.BRIGHT + f"Welcome, {user_name}! Let's give your text some AI magic.")
    print(Fore.YELLOW + Style.BRIGHT + "\nPlease enter the text you'd like to summarize:")
    user_text = input("Enter text: ").strip()
    if not user_text:
        print(Fore.RED + Style.BRIGHT + "No text entered. Exiting.")
    else:
        print(Fore.YELLOW + "\nEnter the model name you want to use :") 
        model_choice = input("Model name (press Enter for default): ").strip()
        if not model_choice:
            model_name = DEFAULT_MODEL
        
        print(Fore.YELLOW + "\nCoose your summarization style:")
        print("1. Standard Summary (Quick & Concise)")
        print("2. Enhanced Summary (More Detailed and Refined)")
        style_choice = input("Enter choice (1 or 2): ").strip()
        if style_choice == "2":
            min_len=80 
            max_len = 200
            print(Fore.BLUE + "Enhancing Summarization Process....")
        else:
            min_len = 50
            max_len = 150
            print(Fore.BLUE + "Usinf Standard Summarization Settings....")
        
        summary = summarize(user_text, min_length=min_len, max_length=max_len, model_name=model_choice)
        if summary:
            print(Fore.GREEN + Style.BRIGHT + f"AI Summarizer Output for {user_name}:")
            print(Fore.CYAN + summary)
        else:
            print(Fore.RED + "Failed to generate a summary.")