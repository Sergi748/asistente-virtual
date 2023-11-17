import os
import json
import pandas as pd
from openai import OpenAI
from functions_calls import *
api_key = 'xxxxxxxxxxxxxx'
os.environ['OPENAI_API_KEY'] = api_key
client = OpenAI(api_key=api_key)


def chat_functions(prompt, id_session, path_context, functions_calls, historical=True, return_resp=False,
                   filename='contexto_chatgpt', model="gpt-3.5-turbo-1106", temperature=0):

    def __get_response(id_session, message, model, temperature):
        response = client.chat.completions.create(
            model=model,
            messages=message,
            temperature=temperature,
            functions=functions_calls['functions_calls'],
            function_call="auto"
            )

        # resp = response["choices"][0]["message"]
        resp = response.choices[0].message

        # if resp.get("function_call"):
        if resp.function_call is not None:
            function_name = resp.function_call.name
            arg = json.loads(resp.function_call.arguments)
            proc_funct = FunctionsCalls(message=message, function_name=function_name, arg=arg)
            message, resp_f = proc_funct.process_functions()
        else:
            resp_f = resp.content.replace('\n', ' ')
            if return_resp is False:
                print(resp_f)
            message.append({"role": "assistant", "content": resp_f})

        df_response = pd.DataFrame(message)
        df_response['session'] = id_session
        df_response = df_response[['session', 'role', 'content']]

        return df_response, resp_f

    if historical:
        df_context_hist = pd.read_csv(os.path.join(path_context, f'{filename}.csv'), sep='|')
        try:
            context = df_context_hist[df_context_hist['session'] == id_session].drop(['session'], axis=1)\
                .to_dict(orient='records')
            df_context_hist = df_context_hist[df_context_hist['session'] != id_session].copy()
        except:
            df_context_hist = pd.DataFrame()
            context = []
    else:
        df_context_hist = pd.DataFrame()
        context = []

    message_user = {"role": "user", "content": prompt}
    context.append(message_user)
    df_context, resp_r = __get_response(id_session=id_session, message=context, model=model, temperature=temperature)

    if historical:
        # Agregamos el nuevo contexto al histórico previamente guardado.
        df_context = pd.concat([df_context_hist, df_context]).reset_index(drop=True).copy()
        df_context.to_csv(os.path.join(path_context, f'{filename}.csv'), sep='|', index=False)

    if return_resp:
        return resp_r
