input("Pressione Enter para iniciar o chatbot...")

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Carregar o modelo e o tokenizer do GPT-2 Small
print("Carregando o modelo...")
tokenizer = AutoTokenizer.from_pretrained("gpt2-small")
model = AutoModelForCausalLM.from_pretrained("gpt2-small")

# Configuração da memória de contexto
context_memory = []
MAX_CONTEXT_LENGTH = 5  # Limite de interações armazenadas na memória
MAX_RESPONSE_LENGTH = 100  # Limite para a resposta gerada

def chatbot_response(prompt, context_memory):
    # Construir o contexto completo com a memória
    context_text = " ".join(context_memory) + prompt
    inputs = tokenizer.encode(context_text, return_tensors="pt")

    # Gerar a resposta sem gradientes para otimizar a memória
    with torch.no_grad():
        outputs = model.generate(inputs, max_length=MAX_RESPONSE_LENGTH, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

print("Chatbot iniciado! (Digite 'sair' para encerrar)")
while True:
    try:
        user_input = input("Você: ")
        if user_input.lower() == "sair":
            print("Chatbot: Até mais!")
            break

        # Adicionar a entrada do usuário ao contexto
        prompt = f"Você: {user_input}\nChatbot:"
        response = chatbot_response(prompt, context_memory)
        print(f"Chatbot: {response}")

        # Atualizar a memória de contexto
        context_memory.append(f"Você: {user_input}")
        context_memory.append(f"Chatbot: {response}")

        # Limitar o tamanho da memória de contexto
        if len(context_memory) > MAX_CONTEXT_LENGTH * 2:
            context_memory = context_memory[-MAX_CONTEXT_LENGTH * 2:]

    except Exception as e:
        print(f"Erro: {e}")
        input("Pressione Enter para fechar o programa.")
        break

# Pausa final para garantir que o programa não feche automaticamente
input("Pressione Enter para encerrar o programa.")
