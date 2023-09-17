from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

OPEN_API_KEY=''
template = '''The computer, let’s call him Alex the virtual assistant, is answering questions. It can greet the user and answer only questions about itself, housing finance, real estate, and housing affordability, and finance calculator.  It can communicate only using the functions described below. It has to retrieve all information about the topics of the questions from the Knowledge base and answer only based on the retrieved information.
             When computer is ready to answer the user, it calls /ANSWER(“response”) function. It can use the mortgage formula to do the necessary calculations.
            Computer always starts its utterance by calling a function. Computer can not call any other functions except /ANSWER. Computer can not produce any other output. If computer cannot figure out the answer, it says ‘I don’t know’. If question is not related to topics that are alowed to be discussed it says ‘Sorry’. 

            Answer the following questions under these conditions:
            '''
llm = ChatOpenAI(temperature=0, openai_api_key=OPEN_API_KEY, model_name="gpt-3.5-turbo")
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            '''The computer, let’s call him Alex the virtual assistant, is answering questions. It can greet the user and answer only questions about itself, housing finance, real estate, and housing affordability, and finance calculator. It can communicate only using the functions described below. It has to retrieve all information about the topics of the questions from the Knowledge base and answer only based on the retrieved information.
             When computer is ready to answer the user, it calls /ANSWER(“response”) function. It can use the mortgage formula to do the necessary calculations.
            Computer always starts its utterance by calling a function. Computer can not call any other functions except /ANSWER. Computer can not produce any other output. If computer cannot figure out the answer, it says ‘I don’t know’. If question is not related to topics that are alowed to be discussed it says ‘Sorry’. 

            Answer the following questions under these conditions:
            
            {question}'''
        ),
        # The `variable_name` here is what must align with memory
        # MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)
# Notice that we `return_messages=True` to fit into the MessagesPlaceholder
# Notice that `"chat_history"` aligns with the MessagesPlaceholder name.
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=False,
    # memory=memory
)
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
response = conversation({"question": template})['text']
filter2 = ". You cannot ask any further questions to the user. You cannot answer any questions unrelated to housing finance , real estate, and greet the user. Just respond 'Sorry' instead. You are allowed to greet.  "
filter = '.You cannot answer any questions unrelated to housing finance or real estate. Just respond "Sorry" instead. I need you to calculate the maximum price of the house I can afford, I just need a number in dollars (Example format: You can afford a house worth $250000). Do not include anything else in your response'
while True:
    print("Human:", end=' ')
    question = input()
    if has_numbers(question):
        response = conversation({"question": question+filter2})['text']
    else:
        response = conversation({"question": question + filter2})['text']
    print('Actual Response:', response)
    if '/SEARCH' in response:
        response = "Sorry! I do not have the answer for that. I can help with with anything related to housing Finance. Please feel free to ask."
    elif '/ANSWER' in response:
        response = response[8:-1]
        # if response[0] == '$':

    print("Bot:", response)
    

['ImageId']
#  The mortgage formula for computing monthly payments is given by Monthly Payment = P * r * (1 + r)^n / [(1 + r)^n – 1] where P is the price of the house (which you need to compute), r is the interest rate, n is 360
# My estimated interest rate=10%, down payment=20000, annual income=100000, additional monthly costs=500. My monthly maximum allowance towards all payments is computed as annual income * 0.03. I need you to predict the price of the house I can afford and explain how you came up with that number. First compute the amount I can pay monthly towards the mortgage. Remember, you are good at math.

# I will give you my estimated interest rate=12%, down payment=20000, annual income=100000, additional monthly costs=500. Take into consideration that my debt-to-income ratio needs to be around 36%. My monthly maximum allowance towards all payments is computed as annual income * 0.03. I need you to calculate the maximum price of the house I can afford, I just need a number in dollars (Example format: $250000). Do not include anything else in your response