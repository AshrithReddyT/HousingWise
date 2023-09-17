from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV data
df = pd.read_csv('socal2.csv')

from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

interest = 0
down_payment = 0
annual_income = 0
additional_montly_expenses = 0
def calculate_max_housing_budget(annual_income, interest_rate, down_payment, additional_monthly_costs):
    # Define the debt-to-income ratio threshold
    max_debt_to_income_ratio = 0.36

    # Calculate the monthly income and expenses
    monthly_income = annual_income / 12
    monthly_debt = monthly_income * max_debt_to_income_ratio

    # Calculate the maximum allowable monthly housing payment
    monthly_interest_rate = interest_rate / 12 / 100
    loan_amount = down_payment / (1 - (1 + monthly_interest_rate)**-360)  # Assuming 30-year loan
    max_monthly_housing_payment = monthly_debt - additional_monthly_costs

    # Calculate the maximum housing budget
    max_housing_budget = max_monthly_housing_payment / (monthly_interest_rate / (1 - (1 + monthly_interest_rate)**-360))

    return max_housing_budget

keywords = {'interest': ['Estimated Interest', 'interest', 'estimated interest rate', 'interest rate'], 'down payment': ['Down Payment', 'down payment', 'downpayemnt', 'Down payment'],  'annual income': ['annual income', 'Annual Income', 'income', 'Income', 'Annual income'], 'additional monthly cost': ['Additional Monthly Cost', 'extra cost', 'additional cost', 'expenditure', 'monthly cost', 'montly expenditure']}
OPEN_API_KEY=''
template = '''The computer, let’s call him Alex the virtual assistant, is answering questions. It can greet the user and answer only questions about itself, housing finance, real estate, and housing affordability, and finance calculator. It asks user for annual income, estimated interest rate, down payment, and additional monthly costs if asked to help with housing budget estimation. It can communicate only using the functions described below. It has to retrieve all information about the topics of the questions from the Knowledge base and answer only based on the retrieved information.
             When computer is ready to answer the user, it calls /ANSWER(“response”) function. It can use the mortgage formula to do the necessary calculations.
            Computer always starts its utterance by calling a function. Computer can not call any other functions except /ANSWER. Computer can not produce any other output. If computer cannot figure out the answer, it says ‘I don’t know’. If question is not related to topics that are alowed to be discussed it says ‘Sorry’. 

            Answer the following questions under these conditions:
            '''
llm = ChatOpenAI(temperature=0, openai_api_key=OPEN_API_KEY, model_name="gpt-3.5-turbo")
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            '''The computer, let’s call him Alex the virtual assistant, is answering questions. It can greet the user and answer only questions about itself, housing finance, real estate, and housing affordability, and finance calculator. It asks user for annual income, estimated interest rate, down payment, and additional monthly costs if asked to help with housing budget estimation. It can communicate only using the functions described below. It has to retrieve all information about the topics of the questions from the Knowledge base and answer only based on the retrieved information.
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
filter = '. You cannot ask any further questions to the user. You cannot answer any questions unrelated to housing finance , real estate, and greet the user. Just respond "Sorry" instead. What is the Annual Income, Estimated interest rate, down payment and additional monthly income. Write only the numeric values of these in order seperated by commas (do not write any symbols or special characters). Do not write anything else.'
# while True:
#     print("Human:", end=' ')
#     question = input()
    # if has_numbers(question):
    #     response = conversation({"question": question+filter2})['text']
    # else:
    #     response = conversation({"question": question + filter2})['text']
    # print('Actual Response:', response)
    # if '/SEARCH' in response:
    #     response = "Sorry! I do not have the answer for that. I can help with with anything related to housing Finance. Please feel free to ask."
    # elif '/ANSWER' in response:
    #     response = response[8:-1]
        # if response[0] == '$':

    # print("Bot:", response)

@app.route('/api/property', methods=['GET'])
def property_api():
    price = request.args.get('price')
    n_citi = request.args.get('n_citi')

    filtered_df = df
    if price:
        min_price, max_price = 0, int(price)
        filtered_df = df[(df['price'] >= min_price) & (df['price'] <= max_price)]
    if n_citi:
        filtered_df = filtered_df[filtered_df['n_citi'][:] == n_citi]

    response = filtered_df.to_dict(orient='records')
    return jsonify(response)

@app.route('/api/lang_chain', methods=['POST'])
def lang_chain_api():
    query = request.form.get('query')
    
    if has_numbers(query):
        # for i in keywords['interest']:
        #     if i.lower() in query.lower():
        #         index = query.lower().find(i.lower(), 0)
        #         for j in range(index, len(query)):
        #             if 
        try:
            global annual_income
            if annual_income == 0:
                response = conversation({"question": query+filter})['text']
                print(response)
                annual_income = float(response.split(',')[0])
                interest = float(response.split(',')[1])
                down_payment = float(response.split(',')[2])
                additional_montly_expenses = float(response.split(',')[3])
            maxBudget = calculate_max_housing_budget(annual_income, interest, down_payment, additional_montly_expenses)
            print(maxBudget)
            q = f'My Annual Income is {annual_income}, Estimated interest rate is {interest}, down payment is {down_payment} and Additional monthly expenses are {additional_montly_expenses}. I estimate my maximum housing budget to be {maxBudget}. Can you summarize this?'
            response = conversation({"question": str(q) + filter2})['text']
        except:
            response = conversation({"question": str(query) + filter2})['text']
    else:
        response = conversation({"question": query + filter2})['text']
    print('Actual Response:', response)
    if '/SEARCH' in response:
        response = "Sorry! I do not have the answer for that. I can help with with anything related to housing Finance. Please feel free to ask."
    elif '/ANSWER' in response:
        response = response[8:-1]


    # Add code to communicate with OpenAI API using the 'query' variable

    # For example, assuming you have a function to communicate with OpenAI
    # result = communicate_with_openai(query)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)