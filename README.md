# whatsapp-chat-agent

This project demonstrates the core functionality of a WhatsApp chat routing system, including session management and automated agent assignment.


Please ensure you have Python 3.8+ installed on your system. You can check your version by running:

`python --version`


1. Installation
   
   Clone the repository:
   
   `git clone https://github.com/SabrinaChuo/whatsapp-chat-agent.git`
   
   `cd whatsapp-chat-agent`


   Install dependencies:

   `pip install -r requirement.txt`

   
3. Configuration

   Create a `.env` file in the root directory by copying the `.env.sample`:

   `cp .env.sample .env`

   Open the `.env` file and set your `SECRET_TOKEN`:

   `SECRET_TOKEN=add_your_token_here`
   
5.  Database initialization
    Run database initialization to create database table:

    `python database.py`

    
6. Run the application

   Start FastAPI using Uvicorn:
  
    `uvicorn main:app --reload`
  
