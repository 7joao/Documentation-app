import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Set up the page configuration
st.set_page_config(
    page_title="Klinisk Dokumentation Dashboard"
)
# Title of the app
st.title("Välkommen till prototypen för Klinisk Dokumentation!")
st.write("Utforska sätt att optimera klinisk dokumentation för att spara tid för kliniker.")

# Text explaining the concept
st.write("Utforska hur journalföring kan optimeras för att spara tid för kliniker.")
st.write("Utforska hur Patientrapporterade Resultatmått (PROMs) kan inkluderas i behandlingsresan för att skapa en grund för evidensbaserad vård!")

# Sidebar - Navigation
st.sidebar.title("Navigation")

# Add a radio button to choose the page
page = st.sidebar.radio("Välj en sida:", ["Första Bedömning", "PROM Data", "Analyserbara Insikter"])


Ct_codes = {
    "Pre-amputation estimated body height (observable entity)": 1162417005,
    "Dominant hand (attribute)": 263557007,
    "Weakness of left hand (finding)": 15639641000119109,
    "Weakness of right hand (finding)": 13530001000004108,
    "Weakness of bilateral hands (finding)": 15639681000119104,
    "Use of aids for daily life": 183364001,
    "Functional independence measure": 273469003,
    "Independent with dressing": 129035000,
    "Independent feeding": 165224005,
    "Independent for personal grooming": 704437004,
    "Ability to perform personal hygiene activity": 284779002,
    
    "Living Conditions/Environment": {
        "Apartment": 257564005,
        "Personal care assistance at home": 105389006,
        "Home well personalized": 224266002,
        "Home poorly personalized": 224267006,
        "House": 257630004,
        "Personal care assistance at home": 105389006,
        "Home well personalized": 224266002,
        "Home poorly personalized": 224267006,
        "Nursing home": 42665001
    },
   "Amputation Level": {
        "Shoulder disarticulation": 88310008,
        "Transhumeral amputation": 88318006,
        "Transradial amputation": 88317007,
        "Partial hand amputation": 88319005,
        "Complete hand amputation": 88320000,
        "Partial forearm amputation": 88321005,
        "Complete arm amputation": 88322004
    },
    "Side": {
        "Amputation of right upper extremity": 723315006,
        "Amputation of left upper extremity": 723314005,
        "Amputation of bilateral upper limbs": 895470004,
        "Amputation of bilateral arms through humerus": 1269448002,
        "Amputation of bilateral forearms through radius and ulna": 895471000,
        "Amputation of bilateral hands": 895473002
    },
    "Type": {
        "Traumatic": 1078289006,
        "Congenital": 205161004
    },
    "Working Conditions": {
        "Stopped work": 160895006,
        "Retired, life event": 105493001,
        "Working, function": 261041009,
        "Full-time employment": 160903007,
        "Part-time employment": 160904001
    },
    
    "Pos-Amputation": {
        "Prosthesis Interest": {
            "Interested": 225469004,
            "Lack of interest": 713566001
        },
        "Expectations": {
            "Fit for work": 160926000,
            "Ability to engage in a hobby": 300755007,
            "Ability to perform creative activity": 300761005,
            "Ability to perform gardening activities": 300749002,
            "Ability to perform play and sports activities": 300767009,
            "Ability to use public recreational facilities": 300743001
        },
        "Pain and Stump Conditions": {
            "Phantom pain following amputation of upper limb": 711058008,
            "Edema of amputation stump of upper limb": 1255168008
        },
        "Stump Care & Techniques": {
            "Impaired skin integrity": 7919002,
            "Care of stump technique": 229612001,
            "Application of conical pressure bandage to amputation stump": 802591000000104
        }
    },
    
    "Cognitive and Psychological Status": {
        "Good cognitive ability": 413384008
    }
}


# Conditional content based on selected page
if page == "Första Bedömning":
    st.title("Första Bedömning Efter Amputation av Övre Extremitet")
    st.write("Välkommen till sidan för Första Bedömning!")
    st.write("Välj flera alternativ för att skapa en klinisk anteckning (t.ex., i detta fall första bedömning efter amputation av övre extremitet).")
    st.write("Den kliniska anteckningen skulle skapas utan att klinikern behöver skriva allt manuellt, och täcker de huvudsakliga aspekterna som vanligtvis diskuteras. Klinikern kan sedan granska och göra ändringar om det behövs.")

    # Define the available amputation types
    amputation_types = {1: "Traumatisk", 2: "Medfödd"}
    # Display the available amputation types in a selectbox
    st.write("### Amputationstyp")
    answer_type = st.radio("Vänligen välj amputationstyp:", options=list(amputation_types.values()))
    # Initialize an empty list to store the selected type
    type_f = []
    # Check the selected type and append the corresponding value
    if answer_type == "Traumatisk":
        type_f.append(amputation_types[1])  # Append 'traumatic'
    elif answer_type == "Medfödd":
        type_f.append(amputation_types[2])  # Append 'congenital'
    # Define the dictionaries for meeting place
    place = {
    1: "Klinik (ForMotion)", 
    2: "Sjukhus"
    }
    # Display the available meeting places in a radio button
    st.write("### Mötesplats")
    answer_place = st.radio("Vänligen välj mötesplats:", options=list(place.values()))
    # Initialize an empty list to store the selected place
    place_f = []
    # Check the selected place and append the corresponding value
    if answer_place == "Klinik (ForMotion)":
        place_f.append(place[1])  # Append 'clinic'
    elif answer_place == "Sjukhus":
        place_f.append(place[2])  # Append 'hospital'
    # Define the cognition levels
    cognition = {
    1: "bra kognition", 
    2: "dålig kognition"
    }

    # Display the available cognition levels in a radio button
    st.write("### Kognitionsnivå")
    answer_cognition = st.radio("Vänligen välj kognitionsnivå:", options=list(cognition.values()))

    # Initialize an empty list to store the selected cognition
    cognition_f = []

    # Check the selected cognition level and append the corresponding value
    if answer_cognition == "bra kognition":
        cognition_f.append(cognition[1])  # Append 'good cognition'
    elif answer_cognition == "dålig kognition":
        cognition_f.append(cognition[2])  # Append 'bad cognition'
    # Define the interest levels in prosthesis
    intereste = {
    1: "positiv", 
    2: "negativ"
    }

    # Display the available interest levels in a radio button
    st.write("### Intresse för Protes")
    answer_intereste = st.radio("Vänligen välj ditt intresse för protes:", options=list(intereste.values()))

    # Initialize an empty list to store the selected interest
    intereste_f = []

    # Check the selected interest level and append the corresponding value
    if answer_intereste == "positiv":
        intereste_f.append(intereste[1])  # Append 'positive'
    elif answer_intereste == "negativ":
        intereste_f.append(intereste[2])  # Append 'negative'

    # Define the available amputation side options
    side = {
        1: "Amputation av höger övre extremitet", 
    2: "Amputation av vänster övre extremitet", 
    3: "Bilateral amputation av övre extremiteter", 
    4: "Amputation av båda armarna genom humerus", 
    5: "Amputation av båda underarmarna genom radius och ulna", 
    6: "Amputation av båda händerna"
    }

    # Display the available amputation sides in a radio button
    st.write("### Amputationssida")
    answer_side = st.radio("Vänligen välj sida för amputation:", options=list(side.values()))

    # Initialize an empty list to store the selected side
    side_f = []

   # Check if the selected side is valid (exists in the dictionary)
    if answer_side in side.values():
        side_f.append(answer_side)  # Append the selected amputation side
    
    # Define the available amputation levels
    level = {
    1: "Axeldesartikulation", 
    2: "Transhumeral amputation", 
    3: "Transradial amputation", 
    4: "Partiell handamputation", 
    5: "Komplett handamputation"
    }

    # Display the available amputation levels in a radio button
    st.write("### Amputationsnivå")
    answer_level = st.radio("Vänligen välj amputationsnivå:", options=list(level.values()))

    # Initialize an empty list to store the selected level
    level_f = []

    # Check if the selected level is valid (exists in the dictionary)
    if answer_level in level.values():
        level_f.append(answer_level)  # Append the selected amputation level
    else:
        st.write(f"Please select a valid option from {list(level.keys())}")


    # Function to display the assessment questions and get responses
    def get_patient_assessment_2(assessment_name):
        valid_range = ("Ja", "Nej")  # The only valid responses are "Yes" or "No"
    
        # Display the question
        st.write(f"### {assessment_name}")
    
        # Take user input using radio buttons
        assessment_value = st.radio(f"Är patienten {assessment_name.lower()}?", options=valid_range)

        if assessment_value == "Ja":
         if assessment_name == "använder hjälpmedel i vardagen":
            st.write(f"Patienten rapporterar att de ofta använder hjälpmedel i vardagen.")
        elif assessment_value == "Nej":
         if assessment_name == "använder hjälpmedel i vardagen":
            st.write(f"Patienten rapporterar att de inte använder hjälpmedel i vardagen.")
    
        return assessment_value  # Return the user's response for storage

    # List of assessments (you can add more assessments here as needed)
    assessments = [
     "Självständig med påklädning",
    "Självständig vid måltider",
    "Självständig med personlig vård",
    "Förmåga att utföra personlig hygien",
    "Använder hjälpmedel i vardagen",
    "Lämplig för arbete",
    "Förmåga att utöva en hobby",
    "Förmåga att utföra kreativ aktivitet",
    "Förmåga att utföra trädgårdsarbete",
    "Förmåga att delta i lek och sportaktiviteter",
    "Förmåga att använda offentliga rekreationsanläggningar",
    ]

    # List to store the answers
    Answers_2 = []  

    # Loop through each assessment and call the generalized function
    for assessment_name in assessments:
      response = get_patient_assessment_2(assessment_name)  # Get the response from the patient
      Answers_2.append((assessment_name, response))  # Store the response along with the assessment name

    # Now, add the "Generate Clinical Note" button only on this page
    if st.button('Generera kliniska anteckningar'):
        # Generate the clinical note content
        st.session_state.clinical_note = ""  # Reset the note for a new generation

        # Append the patient's first post-amputation visit information
        st.session_state.clinical_note += f"Mötte patient med {level_f[0]} vid {place_f[0]} för första besöket efter amputation.\n"
        st.session_state.clinical_note += f"Patienten har en {side_f[0]} av {type_f[0]} etiologi.\n"

        # Append prior reports from the assessment
        st.session_state.clinical_note += "Frågade patienten om deras förmågor före amputationen, varpå de rapporterar:\n"
        for report in Answers_2:
            st.session_state.clinical_note += f"- {report[0]}: {report[1]}\n"

        # Append cognition and interest in prosthesis
        st.session_state.clinical_note += f"Patienten verkar ha {cognition_f[0]} och förståelse för situationen. Vid fråga om protes visar patienten {intereste_f[0]} intresse.\n"

        # Append the final follow-up statement
        st.session_state.clinical_note += "Uppföljning för att diskutera framtida steg är inplanerad."

        # Now display the full clinical note
        st.text_area("Kliniska anteckningar:", st.session_state.clinical_note, height=300)


#if st.button("Display coded clinical note"):
    # Ensure the clinical note exists before replacing
    #if st.session_state.clinical_note:
        # Iterate through the Ct_codes dictionary and replace keys with corresponding values in the clinical note
        #for key, value in Ct_codes.items():
            #st.session_state.clinical_note = st.session_state.clinical_note.replace(key, str(value))  # Replace key with its corresponding value

        # Display the modified clinical note
        #st.write(st.session_state.clinical_note)
    #else:
        #st.write("No clinical note generated yet.")


elif page == "PROM Data":
    st.title("Exempel på PROM-baserade data")
    st.write("Välkommen till PROM-datasidan!")
    st.write("Exempel på hur PROM-baserade data skulle visas.")
    st.write("Detta möjliggör kvantifiering av behandlingseffekter och förståelse för hur komponentförändringar (t.ex. en ny protesknäled) påverkar patientens välbefinnande.")
    st.write("Nedan finns information om patienten Markus (varje patient kommer att ha sin egen flik).")
    st.write("Detta kommer att bidra till att bättre motivera komponentförskrivning och få tillstånd för dyrare alternativ.")


    # Set up the seed for reproducibility (optional)
    np.random.seed(42)

    # Define the ranges or possible values for the variables
    life_quality_range = ['1', '2', '3', '4', '5', '6', '7', '8']
    prosthesis_types = ['1', '2']  # Prosthesis types
    mobility_levels = ['1', '2', '3', '4']
    satisfaction_levels = ['1', '2', '3', '4', '5']
    Prosthesis_socket = ['3D-printad', 'Direct socket', 'Konventionell']
    Prosthesis_knee = ['MPK', 'non-MPK']
    Prosthesis_feet = ['Sach', 'Energy return', 'Eletronic']

    # Define the number of rows for the simulated data
    num_rows = 2  # You can change this number as needed

    # Create random data for the table
    data = {
    'Life Quality': np.random.choice(life_quality_range, num_rows),
    'Prosthesis': prosthesis_types,
    'Prosthesis_socket': np.random.choice(Prosthesis_socket, num_rows),
    'Prosthesis_knee': np.random.choice(Prosthesis_knee, num_rows),
    'Prosthesis_feet': np.random.choice(Prosthesis_feet, num_rows),
    'Mobility Level': np.random.choice(mobility_levels, num_rows),
    'Satisfaction Level': np.random.choice(satisfaction_levels, num_rows),
    }

    # Create a DataFrame using pandas
    df = pd.DataFrame(data)
    df

    # Visualization: Mobility Level per Prosthesis Type
    st.write("### Rörelsenivå per protes")



    df['Mobility Level'] = pd.Categorical(df['Mobility Level'], categories=['1', '2', '3', '4'], ordered=True)

    # Plotting scatter plot where X = Prosthesis, Y = Mobility Level
    sns.scatterplot(x='Prosthesis', y='Mobility Level', data=df, hue='Prosthesis', palette='Set1', s=100)

    # Set the y-axis to show all possible mobility levels (1 to 4)
    plt.yticks([0, 1, 2, 3], ['1', '2', '3', '4'])  # Justera för att visa de kategoriska nivåerna korrekt
    plt.gca().invert_yaxis()  # Valfritt, om du vill ha högre nivåer högst upp

    # Adding labels and title
    plt.title("Spridningsdiagram över rörelsenivå per protes")
    plt.xlabel("Protes")
    plt.ylabel("Rörelsenivå (K-Nivå)")
    st.pyplot(plt)
    st.write("Med PROM-data kan man se att efter att ha bytt till protes 2, gick den beräknade K-nivån ner.")
    st.write("Genom att analysera vad som förändrades (komponenterna i den nya protesen) är det möjligt att bättre förstå varför och motivera behovet av förändring.")




    

    st.write("### Livskvalitet per protes")

    # Reset the figure to ensure no previous plots are interfering
    plt.figure(figsize=(10, 6))

    # Assuming 'Life Quality' is categorical (e.g., '1' to '8') in your DataFrame
    df['Life Quality'] = pd.Categorical(df['Life Quality'], categories=['1', '2', '3', '4', '5', '6', '7', '8'], ordered=True)

    # Plotting scatter plot where X = Prosthesis, Y = Life Quality
    sns.scatterplot(x='Prosthesis', y='Life Quality', data=df, hue='Prosthesis', palette='Set1', s=100)

    # Set the y-axis to show all possible life quality levels ('1' to '8')
    plt.yticks([0, 1, 2, 3, 4, 5, 6, 7], ['1', '2', '3', '4', '5', '6', '7', '8'])  # Adjust for correct categorical levels
    plt.gca().invert_yaxis()  # Optional, if you want higher levels at the top

    # Adding labels and title
    plt.title("Spridningsdiagram över livskvalitet per protes")
    plt.xlabel("Protes")
    plt.ylabel("Livskvalitet")

    # Display the plot
    st.pyplot(plt)
    st.write("Samma tankesätt kan implementeras här för att förstå varför livskvaliteten har minskat efter bytet av protes.")
    st.write("Att inkludera denna information informerar kliniker bättre om sina patienter och möjliggör en bättre behandling, vilket leder till högre nöjdhet och bättre resultat för patienterna.")








elif page == "Analyserbara Insikter":
    st.title("Användning av data för att generera riktlinjeinsikter")
    st.write("Välkommen till sidan för Analyserbara Insikter!")
    st.write("Exempel på hur PROM-baserad data och journaldata kan användas för att generera analyserbara insikter.")
    st.write("När kliniker använder journalmallar på första sidan, är alla alternativ kopplade till internationellt accepterade medicinska kodsystem.")
    st.write("Detta gör att data från alla kliniker kan förstås oavsett språk.")
    st.write("Dessa insikter kan sedan användas för att skapa riktlinjer för behandling baserat på bevis från verkliga situationer.")



    # Set up the seed for reproducibility (optional)
    np.random.seed(42)

    # Define the ranges or possible values for the variables
    Patient_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    Amputation_type = ['79733001', '265736004', '88312006', '397218006', '180030006']
    Amputation_cause = ['262595009', '205386003', '46635009 ', '40713004', '3947001']
    Amputation_Side = ['732213003', '732214009', '732212008']
    life_quality_range = ['1', '2', '3', '4', '5', '6', '7', '8']
    prosthesis_types = [1, 2, 3]  # Prosthesis types
    mobility_levels = ['1', '2', '3', '4']
    satisfaction_levels = ['1', '2', '3', '4']
    Prosthesis_socket = ['3D-printad', 'Direct socket', 'Konventionell']
    Prosthesis_knee = ['MPK', 'non-MPK']
    Prosthesis_feet = ['Sach', 'Energy return', 'Eletronic']

    # Define the number of rows for the simulated data
    num_rows = 50  # You can change this number as needed

    # Create random data for the table
    data = {
    'Life Quality': np.random.choice(life_quality_range, num_rows),
    'Prosthesis': np.random.choice(prosthesis_types, num_rows),
    'Prosthesis_socket': np.random.choice(prosthesis_types, num_rows),
    'Prosthesis_knee': np.random.choice(prosthesis_types, num_rows),
    'Prosthesis_feet': np.random.choice(prosthesis_types, num_rows),
    'Mobility Level': np.random.choice(mobility_levels, num_rows),
    'Satisfaction Level': np.random.choice(satisfaction_levels, num_rows),
    'Patient_id': np.random.choice(satisfaction_levels, num_rows),
    'Amputation_type': np.random.choice(satisfaction_levels, num_rows),
    'Amputation_cause': np.random.choice(satisfaction_levels, num_rows),
    'Amputation_Side': np.random.choice(satisfaction_levels, num_rows),
    }

    # Create a DataFrame using pandas
    df = pd.DataFrame(data)

    # Display the table in the Streamlit app
    st.write("### Simulated Patient Data Table")
    st.dataframe(df)  # Display the table
    st.write("Här kommer information för alla behandlade patienter att organiseras på ett sätt som möjliggör analys.")
    st.write("Med i informationen finns data från PROMs och från användningen av mallar, som den på första sidan, för att skapa kliniska anteckningar.")
    st.write("Alla alternativ som presenteras för kliniker vid skapande av anteckningar är kopplade till internationellt accepterade kodsystem, vilket gör det enkelt att implementera detta system i alla kliniker globalt.")
    st.write("Ju fler kliniker som använder det, desto mer data genereras, vilket gör det möjligt att säkerställa att alla patienter får samma typ av vård oavsett plats.")
    st.write("Mönster kommer att utforskas (till exempel liknande fall som de vi såg med Markus, där en förändring av protes ledde till en nedgång i rörelsenivå och livskvalitet).")
    st.write("För mönster kan riktlinjer för vård skapas, inte för att tala om för kliniker vad de ska göra, utan för att visa vad de kan förvänta sig av sina val.")
    st.write("Det blir möjligt för kliniker att lägga in sina patienters information och se hur behandlingsval (till exempel att byta knäled) kan påverka flera variabler, som rörelsenivå.")
    st.write("Dokumentering av förväntade resultat för dyrare komponenter baseras då på data snarare än vad varje kliniker subjektivt förväntar sig.")


