import streamlit as st
import pandas as pd
import base64
import datetime
import pymongo
import hmac
#from bson import ObjectId

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

sex_mapping = {'male': 0, 'female': 1}
answers = {}




st.markdown(
        """<style>
        div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 20px;
                }
        </style>
                """, unsafe_allow_html=True)


st.markdown(
    """
    <style>
    .centered_button {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)





st.sidebar.header('Informations')

#slider_values = [1,2,3,4]

#slider_strings = ["Très insuffisant", "Insuffisant", "Satisfaisant", "Très satisfaisant"]


def stringify(i:int = 0) -> str:
    return slider_strings[i-1]


def write_data(new_data):
    db = client.Questionnaire
    db.General.insert_one(new_data)
    
#def read_from_file(file_path):
#    with open(file_path, "r", encoding="utf-8") as file:
#        comp_list = [line.strip() for line in file]
#    return comp_list

def read_data_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    all_lists = [item.strip() for item in file_content.split("***")]
    print(all_lists)

    return all_lists

all_data = read_data_file("questionnaire.txt")

st.write(f"""
# {all_data[0]}
""")

all_questions = all_data[1].split("\n\n")
loop = len(all_questions)
if(loop==1):
    Comp = all_data[1].split("\n")


slider_strings = all_data[2].split("\n")
slider_values = [i for i in range(1, len(slider_strings) + 1)]

def user_input_features():
        #current_date = datetime.date.today()
        surname = st.sidebar.text_input("Nom")
        name = st.sidebar.text_input("Prénom")
        date = st.sidebar.date_input("Date de naissance", datetime.date(2010, 1, 1))
        #age = current_date.year - date.year - ((current_date.month, current_date.day) < (date.month, date.day))
        sex = st.sidebar.selectbox('Sex',('Homme','Femme'))
        #study = st.sidebar.selectbox("Niveau d'etude",('CAP/BEP','Baccalauréat professionnel','Baccalauréat général', 'Bac +2 (DUT/BTS)', 'Bac +3 (Licence)',
        #                                               'Bac +5 (Master)', 'Bac +7 (Doctorat, écoles supérieurs)'))
        #questionnaire = st.sidebar.selectbox('Questionnaire',('TRAQ','FAST','TRAQ+FAST'))
        #st.write("""## Concernant mon utilisation de la planche de transfert:""")
        if (loop == 1):
            param = Comp[0]
            Comp = Comp[1:]
            for i, question in enumerate(Comp, start=1):
                slider_output = st.select_slider(
                #f":red[{question}]",
                f"{question}",
                options=slider_values,
                value=1,
                format_func=stringify
                )
                answers[f"{param}{i}"] = slider_output
        else:
            for j in range(len(all_questions)):
                Comp = all_questions[j].split("\n")
                param = Comp[0]
                Comp = Comp[1:]
                for i, question in enumerate(Comp, start=1):
                    slider_output = st.select_slider(
                    f"{question}",
                    options=slider_values,
                    value=1,
                    format_func=stringify
                    )
                    answers[f"{param}{i}"] = slider_output


        user_data = {"lastName": surname,
                     'firstName': name,
                     'birthDate': date.isoformat(),
                     'sex': sex}
                     #'educationalLevel': study}
        answers_data = answers

        document = {
        #"_id": ObjectId(),  # Generate a new ObjectId
        "user": user_data,
        "answers": answers_data
        #"__v": 0
        }
                
        return document



document = user_input_features()

     
     
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    button = st.button('Enregisterez')
    st.image("clinicogImg.png", width=200)
    
if button:
     write_data(document)
     st.write("Merci d'avoir participé(e) à ce questionnaire")
     


     

