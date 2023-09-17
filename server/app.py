from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV data
df = pd.read_csv('socal2.csv')

@app.route('/api/property', methods=['GET'])
def property_api():
    price = request.args.get('price')
    n_citi = request.args.get('n_citi')

    filtered_df = df
    if price:
        min_price, max_price = 0, int(price)
        filtered_df = df[(df['price'] >= min_price) & (df['price'] <= max_price)]
    if n_citi:
        filtered_df = filtered_df[filtered_df['n_citi'] == n_citi]

    response = filtered_df.to_dict(orient='records')
    return jsonify(response)

@app.route('/api/lang_chain', methods=['POST'])
def lang_chain_api():
    query = request.form.get('query')
    
    # Add code to communicate with OpenAI API using the 'query' variable

    # For example, assuming you have a function to communicate with OpenAI
    # result = communicate_with_openai(query)
    
    return jsonify({'response': 'Result from OpenAI'})

if __name__ == '__main__':
    app.run(debug=True)