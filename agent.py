def get_agent_type(message: str) -> str:
    text = message.lower()

    sales= ["price", "buy", "purchase", "cost", "product", "pricing", "order"]
    
    support= ["problem", "issue", "complaint", "broken", "error", "help", "bug", "wrong"]

    for keyword in sales:
        if keyword in text:
            return "sales"
    
    for keyword in support:
        if keyword in text:
            return "support"
    
    return "general"
    
def generate_reply(agent_type: str) -> str:
    if agent_type == "sales":
        return "Thanks for your interest. Can you share what you are looking for?"
    elif agent_type == "support":
        return "Sorry that you are facing this issue. Can you desribe more about your issue?"
    else:
        return "How can I assist you?"