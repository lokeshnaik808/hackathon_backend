from openai import OpenAI
from flask import Flask, request, Response, make_response
from typing import Union
from fastapi import FastAPI, request, Response, make_response
from fastapi.middleware.cors import CORSMiddleware
from flask_cors import CORS, cross_origin
import pandas as pd

# Read the CSV file
file_path = 'resources/initiatives_3.csv'  # Replace with the path to your CSV file
df = pd.read_csv(file_path, encoding='latin1')
df['ID'] = range(1, len(df) + 1)

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = OpenAI(
    api_key="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"
)



def generate_prompt():
    return client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {
                "role": "developer",
                "content": "You job is to generate interesting fact points related to sustainability based on user input "
                           "and user contribution to sustainability measures data: " + str(getUserContribution()) +
                                                                                           ". Give a 100 word response and include the line that 'Every bit counts'."
            },
            {"role": "user", "content": "Measure the impact of my contributions?"}
        ]
    )

def generate_prompt_what_difference(context):
    return client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {
                "role": "developer",
                "content": "Your job is generate response about how contribution to the sustainability initiative can make real world impact."
                           "Use context of the sustainibility initiative:" + context + ". Give a 100 word response and remind that every contribution helps."
            },
            {"role": "user", "content": "What difference will it make if I contribute? And how do I contribute?"}
        ]
    )


@app.route("/measure-my-impact", methods=['GET'])
def hello_world():
#    user_message = request.args.get('userMessage', default=None)
    response = generate_prompt()
    message = response.choices[0].message.content
    #return Response(response="test")
    resp = make_response(str(message), 200)
    return resp


def getUserContribution():
    return ("{co2 saved: 70ton,"
            "euros donated: 300"
            "number_of_initiatives_participated: 3},"
            "number_of_times_volunteered: 5",
            "number_of_phones_recycled: 3")


@app.route("/show-initiative", methods=['GET'])
def show_initiatives():
    initiativeID = request.args.get('initiativeID', default=None)
    print(initiativeID)
    result = df[df['ID'] == int(initiativeID)].to_json()
    return str(result)

@app.route("/show-all-initiatives", methods=['GET'])
def show_all_initiatives():
    result = df.to_json()
    return str(result)

@app.route("/call-to-action", methods=['GET'])
def call_to_action_response():
    initiativeID = request.args.get('initiativeID', default=None)
    print(initiativeID)
    print(str(df[df['ID'] == int(initiativeID)]))
    context = str(df[df['ID'] == int(5)][["Challenge", "Call to Action", "Links"]].to_dict())
    response = generate_prompt_what_difference(context)
    message = response.choices[0].message.content
    #return Response(response="test")
    return make_response(str(message), 200)
