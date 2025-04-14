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
page = st.sidebar.radio("Välj en sida:", ["Journal automatisering", "PROM Data", "Analyserbara Insikter"])
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
if page == "Journal automatisering":
    st.title("Journal automatisering")

    # Add template selection dropdown
    template_choice = st.selectbox(
        "Välj vilken mall du vill använda:",
        [
            "Första Bedömning Efter Amputation av Övre Extremitet",
            "Justering av Protes Nedre Extremitet",
            "Leveranse av Nedre Extremitet Protes"
        ]
    )

    # Template 1: Första Bedömning Efter Amputation av Övre Extremitet
    if template_choice == "Första Bedömning Efter Amputation av Övre Extremitet":
        st.title("Första Bedömning Efter Amputation av Övre Extremitet")
        st.write("Välkommen till sidan för Första Bedömning!")
        st.write("Välj flera alternativ för att skapa en klinisk anteckning (t.ex., i detta fall första bedömning efter amputation av övre extremitet).")
        st.write("Den kliniska anteckningen skulle skapas utan att klinikern behöver skriva allt manuellt, och täcker de huvudsakliga aspekterna som vanligtvis diskuteras. Klinikern kan sedan granska och göra ändringar om det behövs.")

        # Define and display input options for amputation type, place, cognition, etc.
        amputation_types = {1: "Traumatisk", 2: "Medfödd"}
        st.write("### Amputationstyp")
        answer_type = st.radio("Vänligen välj amputationstyp:", options=list(amputation_types.values()))

        place = {1: "Klinik", 2: "Sjukhus"}
        st.write("### Mötesplats")
        answer_place = st.radio("Vänligen välj mötesplats:", options=list(place.values()))

        cognition = {1: "bra kognition", 2: "dålig kognition"}
        st.write("### Kognitionsnivå")
        answer_cognition = st.radio("Vänligen välj kognitionsnivå:", options=list(cognition.values()))

        intereste = {1: "positiv", 2: "negativ"}
        st.write("### Intresse för Protes")
        answer_intereste = st.radio("Vänligen välj ditt intresse för protes:", options=list(intereste.values()))

        side = {
            1: "Amputation av höger övre extremitet", 
            2: "Amputation av vänster övre extremitet", 
            3: "Bilateral amputation av övre extremiteter", 
            4: "Amputation av båda armarna genom humerus", 
            5: "Amputation av båda underarmarna genom radius och ulna", 
            6: "Amputation av båda händerna"
        }
        st.write("### Amputationssida")
        answer_side = st.radio("Vänligen välj sida för amputation:", options=list(side.values()))

        level = {
            1: "Axeldesartikulation", 
            2: "Transhumeral amputation", 
            3: "Transradial amputation", 
            4: "Partiell handamputation", 
            5: "Komplett handamputation"
        }
        st.write("### Amputationsnivå")
        answer_level = st.radio("Vänligen välj amputationsnivå:", options=list(level.values()))

        # Function to display and get patient assessment responses
        def get_patient_assessment_2(assessment_name):
            valid_range = ("Ja", "Nej")
            st.write(f"### {assessment_name}")
            assessment_value = st.radio(f"Är patienten {assessment_name.lower()}?", options=valid_range)
            if assessment_value == "Ja":
                st.write(f"Patienten rapporterar att de ofta använder hjälpmedel i vardagen.")
            elif assessment_value == "Nej":
                st.write(f"Patienten rapporterar att de inte använder hjälpmedel i vardagen.")
            return assessment_value

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
            "Förmåga att använda offentliga rekreationsanläggningar"
        ]

        Answers_2 = []
        for assessment_name in assessments:
            response = get_patient_assessment_2(assessment_name)
            Answers_2.append((assessment_name, response))

        # Button to generate clinical note
        if st.button("Generate kliniska anteckningar"):
            clinical_note = ""  # Reset the note for a new generation

            # Append patient's first post-amputation visit information
            clinical_note += f"Mötte patient med {answer_level} vid {answer_place} för första besöket efter amputation.\n"
            clinical_note += f"Patienten har en {answer_side} av {amputation_types[1]} etiologi.\n"

            # Append prior reports from the assessment
            clinical_note += "Frågade patienten om deras förmågor före amputationen, varpå de rapporterar:\n"
            for report in Answers_2:
                clinical_note += f"- {report[0]}: {report[1]}\n"

            # Append cognition and interest in prosthesis
            cognition_mapping = {
            "bra kognition": 1,
            "dålig kognition": 2
             }

            # Match the selected interest value to the correct dictionary key
            intereste_mapping = {
            "positiv": 1,
            "negativ": 2
            }
            clinical_note += f"Patienten verkar ha {cognition[cognition_mapping[answer_cognition]]} och förståelse för situationen. Vid fråga om protes visar patienten {intereste[intereste_mapping[answer_intereste]]} intresse.\n"

            # Append final follow-up statement
            clinical_note += "Uppföljning för att diskutera framtida steg är inplanerad."

            # Display the clinical note directly
            st.text_area("Kliniska anteckningar:", clinical_note, height=300)

    # Template 2: Justering av Protes Nedre Extremitet
    elif template_choice == "Justering av Protes Nedre Extremitet":
        st.title("Justering av Protes Nedre Extremitet")
        st.write("Välj flera alternativ för att skapa en klinisk anteckning.")
        st.write("De vanligaste anledningarna till justering finns med möjlighet att göra extra val baserat på det valda alternativet för att skapa en komplett klinisk anteckning.")
        st.write("Beroende på huvudorsakerna till besöket får ingenjörerna möjlighet att skriva vad de gjorde, vilket enkelt implementeras i anteckningen.")

        # Define reasons for adjustment
        reasons_for_adjustment = {
            1: "Behöver ny komponent (liner)",
            2: "Behöver ny komponent (sleeve)",
            3: "Obehag vid användning",
            4: "Förändrad stumpvolym",
            5: "Dålig passform",
            6: "En annan anledning"
        }

        st.write("### Anledning till besök")
        answer_reason = st.radio("Vänligen välj anledning till besök:", options=list(reasons_for_adjustment.values()))

        reason_1 = [answer_reason]

        # Handle different reason categories with sub-options
        if answer_reason == "Obehag vid användning":
            reasons_for_discomfort = {
                1: "Smärta runt fibulahuvudet",
                2: "Smärta vid tibias distala ände",
                3: "Smärta under stumpen",
                4: "Tryckkänsla vid specifik belastning",
                5: "Allmän ömhet eller irritation i hylsan"
            }
            discomfort_reason = st.selectbox("Välj anledning till obehag:", list(reasons_for_discomfort.values()))
            reason_2 = [discomfort_reason]
            treatment_steps = st.text_input("Vänligen skriv här de steg du vidtog under besöket för att lösa patientens problem:")
        if  answer_reason ==  "En annan anledning":
            visit_reason = st.text_input("Vänligen skriv här anledningen till besöket:")
            treatment_steps_2 = st.text_input("Vänligen skriv här de steg du vidtog under besöket för att lösa patientens problem:")


        if answer_reason == "Förändrad stumpvolym" or answer_reason == "Dålig passform":
            fixable = {
                1: "Kan lösas vid besöket (utan att göra en ny hylsa)",
                2: "Kan inte lösas vid besöket (ny hylsa behöver göras)"
            }
            fix = st.selectbox("Välj vad som gjordes under besöket:", list(fixable.values()))
            reason_3 = [fix]
        

        if answer_reason == "Behöver ny komponent (liner)" or answer_reason == "Behöver ny komponent (sleeve)":
            stock = {
                1: "Hade komponenten patienten behövde i lager (levererades direkt)",
                2: "Hade inte komponenten i lager (ska beställas och levereras när den kommer)"
            }
            stock_answer = st.selectbox("Välj om komponenten fanns i lager:", list(stock.values()))
            stock_f = [stock_answer]

        # Define visit outcomes
        outcome = {
            1: "Löste patientens problem (patienten kommer kontakta oss vid behov)",
            2: "Kunde inte lösa patientens problem. Diskuterade nästa steg och bokade uppföljning"
        }
        st.write("### Besökets utfall")
        outcome_answer = st.radio("Vänligen välj besökets utfall:", options=list(outcome.values()))
        outcome_1 = [outcome_answer]

        # Button to generate clinical note
        if st.button("Generate kliniska anteckningar"):
            clinical_note = ""  # Reset the note for a new generation

            # Append adjustment visit information
            if reason_1 [0] != "En annan anledning":
                clinical_note += f"Patienten besöker oss för justering av protes och rapporterar {reason_1[0]}.\n"
            else:
                clinical_note += f"Patienten besöker oss för justering av protes och rapporterar {visit_reason}.\n"

            if reason_1[0] == "Obehag vid användning":
                clinical_note += f"Vid undersökning rapporterar patienten {reason_2[0]} vid gång.\n"
                clinical_note += f"Under besöket vidtogs följande steg för att justera patientens protes:\n"
                clinical_note += f"{treatment_steps}.\n"
            if reason_1[0] == "En annan anledning":
                clinical_note += f"Under besöket vidtogs följande steg för att justera patientens protes:\n"
                clinical_note += f"{treatment_steps_2}.\n"
            elif reason_1[0] == "Förändrad stumpvolym" or reason_1[0] == "Dålig passform":
                clinical_note += f"Vid besöket bedöms att {reason_3[0]}.\n"
            elif reason_1[0] == "Behöver ny komponent (sleeve)" or reason_1[0] == "Behöver ny komponent (liner)":
                clinical_note += f"Vid besöket {stock_f[0]}.\n"
            if outcome_1[0] == "Löste patientens problem (patienten kommer kontakta oss vid behov)":
                clinical_note += f"Vid slutet av besöket: {outcome_1[0]}.\n"
            else:
                clinical_note += f"Vid slutet av besöket: {outcome_1[0]}.\n"

            # Display the clinical note directly
            st.text_area("Kliniska anteckningar:", clinical_note, height=300)

    # Template e: Leveranse av Nedre Extremitet Protes
    elif template_choice == "Leveranse av Nedre Extremitet Protes":
        st.title("Leveranse av Nedre Extremitet Protes")
        st.write("Välj flera alternativ för att skapa en klinisk anteckning.")
        st.write("Generera journalanteckningar med möjlighet för kliniker att mata in relevant behandlingsinformation (patientrapporterade och funktionella tester) och få automatiska insikter om dem.")
        st.write("Anslutning till tidigare journalanteckningar kan skapas för att bättre automatisera processen. Till exempel kan K-nivå automatiskt bedömas från en första bedömningsmall och senare kopplas till leveransmallen.")

        # Socket fit
        fit = {1:"bra passform", 2:"dåligt passform"}
        st.write("### Hur var hylsan passformen?")
        answer_passform = st.radio("Vänligen välj:", options=list(fit.values()))

        if answer_passform == "dåligt passform":
            compensation = {1: "provade med 1 protes strumpa och det har blivit bättre",
                            2: "provade med 2 protes strumpa och det har blivit bättre",
                            3: "provade med 3 protes strumpa och det har blivit bättre"}
            answer_compensation = st.radio("Välj lösning:", options=list(compensation.values()))

        # Ability to don and doff prosthesis
        put_prothesis = {
            1: "kan göra",
            2: "kan inte göra",
            3: "kan göra men behöver hjälp"
        }

        st.write("### Förmåga att sätta på protesen självständigt.")
        answer_put = st.radio("Vänligen välj:", options=list(put_prothesis.values()))

        # Handle assistance requirement
        if answer_put == "kan göra men behöver hjälp" or answer_put == "kan inte göra":
            assistance = {
                1: "rapporterar att de får hjälp hemma av någon som kan assistera",
                2: "rapporterar att de kan inte få hjälp hemma av någon som kan assistera"
            }
            answer_assistance = st.radio("Vänligen välj hjälpbehov:", options=list(assistance.values()))

        # Patient post-delivery assessment
        def get_patient_post_delivery_assessment(assessment_name):
            valid_range = ("Ja", "Nej")
            st.write(f"### {assessment_name}")
            assessment_value = st.radio(f"Är patienten {assessment_name.lower()}?", options=valid_range)
            return assessment_value

        assessments = [
            "Förmåga att överföra från stol till säng",
            "Förmåga att gå med protes",
            "Förmåga att sitta upp utan stöd",
            "Förmåga att klara trappor",
            "Förmåga att gå på ojämna ytor",
            "Förmåga att delta i sportaktiviteter",
            "Förmåga att hantera smärta och obehag från protesen",
            "Förmåga att genomföra en rullstolsöverföring",
        ]

        Answers_7 = []
        for assessment_name in assessments:
            response = get_patient_post_delivery_assessment(assessment_name)
            Answers_7.append((assessment_name, response))

        
        # Functional tests
        
        performed = {1:"ja", 2:"nej"}
        st.write("### Har patienten genomfört *Time Up and Go Test*?")
        answer_tug = st.radio("Vänligen välj:", options=list(performed.values()), key="tug_test")
        if answer_tug == "ja":
            TUG = st.text_input("Vänligen ange hur lång tid det tog för patienten att genomföra testet i sekunder. Så om det tog 1 minut, 30 sekunder, ange 90).", key="tug_input")
            TUG_NUMBER = int(TUG) if TUG.isdigit() else 0  # Safe conversion

        st.write("### Har patienten genomfört *Four Square Step Test*?")
        answer_four_sq = st.radio("Vänligen välj:", options=list(performed.values()), key="four_square_test")
        if answer_four_sq == "ja":
            four_sq = st.text_input("Vänligen ange hur lång tid det tog för patienten att genomföra testet i sekunder. Så om det tog 1 minut, 30 sekunder, ange 90).", key="four_sq_input")
            four_sq_f = int(four_sq) if four_sq.isdigit() else 0  # Safe conversion

        st.write("### Har patienten genomfört *100 meter walk test*?")
        answer_100_test = st.radio("Vänligen välj:", options=list(performed.values()), key="100_test")
        if answer_100_test == "ja":
            meter_100 = st.text_input("Vänligen ange hur lång tid det tog för patienten att genomföra testet i sekunder. Så om det tog 1 minut, 30 sekunder, ange 90).", key="100_test_input")
            METER_100 = int(meter_100) if meter_100.isdigit() else 0  # Safe conversion
            if METER_100 > 0:
             walking_speed = 100 / METER_100

        # reabbilitation

        rehab = {1: "interesserade", 2: "inte interesserade"}
        st.write("Är patienten intresserad av rehabilitering?")
        rehab_interess = st.radio("Vänligen välj:", options=list(rehab.values()))

        # Handle assistance requirement
        if rehab_interess == "interesserade":
            assistance = {
                1: "vill gå med i gångskola",
                2: "rapporterar att de har tillgång till privat fysioterapi",
                3: "vill ha enskilda sessioner med fysioterapeut"
            }
            answer_assistance = st.radio("Vänligen välj hjälpbehov:", options=list(assistance.values()))

        # Button to generate clinical note
        if st.button("Generate kliniska anteckningar"):
            clinical_note = ""  # Reset the note for a new generation

            # Append adjustment visit information
            clinical_note += f"Patienten besöker oss för leverans av protes.\n"
            clinical_note += f"Vid provning passformen kontrollerades. Hylsan har en {answer_passform}, vilket patienten håller med.\n"
            if answer_passform == "dåligt passform":
                clinical_note += f"För att förbättra passformen {answer_compensation}.\n"
            clinical_note += f"Visade patienten hur man tar på protesen och kontrollerade om de kan göra det självständigt, vilket de {answer_put}.\n"
            if answer_put == "kan inte göra" or answer_put == "kan göra men behöver hjälp":
                clinical_note += f"Frågade patienten och de {answer_assistance}, och att de ska träna för att kunna klara det.\n"
            clinical_note += "Vid besöket kontrollerades om patienten klarade följande aktiviteter:\n"
            for report in Answers_7:
                clinical_note += f"- {report[0]}: {report[1]}\n"
            if answer_100_test == "ja":
                clinical_note += f"Patienten genomförde 100 meter walking testet på {METER_100} sekunder.\n"
                clinical_note += f"Patientens gånghastighet är {walking_speed:.2f} meter per sekund.\n"
            if answer_tug == "ja":
                clinical_note += f"Patienten genomförde TUG-testet på {TUG_NUMBER} sekunder.\n"
                if TUG_NUMBER > 30:
                    clinical_note += "Från TUG performance kan patienten klassificeras som K-nivå: 1 - Begränsad mobilitet, behöver hjälpmedel eller assistans.\n"
                elif 20 <= TUG_NUMBER <= 30:
                    clinical_note += "Från TUG performance kan patienten klassificeras som K-nivå: 2 - Begränsad gemenskapsmobilitet.\n"
                elif 15 <= TUG_NUMBER < 20:
                    clinical_note += "Från TUG performance kan patienten klassificeras som K-nivå: 3 - Gemenskapsmobilitet med varierande hastigheter.\n"
                else:
                    clinical_note += "Från TUG performance kan patienten klassificeras som K-nivå: 4 - Hög mobilitet, möjlig för rekreation eller tävling.\n"
            if answer_four_sq == "ja":
                clinical_note += f"Patienten genomförde Four Square Step-testet på {four_sq_f} sekunder.\n"
                if four_sq_f > 30:
                    clinical_note += ("Från Four Square Step-testet performance kan fallrisken klassificeras som hög. "
                                      "Rekommenderas vidare utvärdering för fallförebyggande åtgärder.\n")
                elif 20 <= four_sq_f <= 30:
                    clinical_note += ("Från Four Square Step-testet performance kan fallrisken bedömas som måttlig. "
                                       "Överväg anpassningar för ökad balans och säkerhet.\n")
                elif 15 <= four_sq_f < 20:
                    clinical_note += ("Från Four Square Step-testet performance kan fallrisken bedömas som låg. "
                                      "Fortsatt övervakning rekommenderas.\n")
                else:
                    clinical_note += ("Från Four Square Step-testet performance kan fallrisken bedömas som mycket låg. "
                                      "Patienten visar god balans och stabilitet.\n")

            if rehab_interess == "interesserade":
                clinical_note += f"Frågade patienten om rehabilitering vilken dem är {rehab_interess} och {answer_assistance}.\n"
            else:
                clinical_note += f"Frågade patienten om rehabilitering vilken dem är {rehab_interess[0]}.\n"
            clinical_note += "Kom överens med patienten att de ska försöka använda protesen så mycket som möjligt och ska kontakta oss vid behov.\n"

            # Display the clinical note directly
            st.text_area("Kliniska anteckningar:", clinical_note, height=300)

elif page == "PROM Data":
    st.title("Exempel på PROM-baserade data")
    st.write("Välkommen till PROM-datasidan!")
    st.write("Exempel på hur PROM-baserade data skulle visas.")
    st.write("Detta möjliggör kvantifiering av behandlingseffekter och förståelse för hur komponentförändringar (t.ex. en ny protesknäled) påverkar patientens välbefinnande.")
   
    st.write("Detta kommer att bidra till att bättre motivera komponentförskrivning och få tillstånd för dyrare alternativ.")
    st.write("Informationen är kopplad till specifika hjälpmedel så att det är lätt för ingenjörer att förstå resultatet varje har haft.")
    st.write("Se hur patientrapporterad data kan användas för att följa framsteg.")
    st.write("Senare kan huvudtriggers läggas till för att automatiskt informera kliniker om patienternas behov (till exempel om komfortnivån sjunker under en viss gräns, får kliniker en påminnelse om att eventuellt kontakta patienter för tillverkning av ny sockel).")
    st.write("Data från patientjournalen (som att utföra specifika funktionella tester) som fylls i i journalen kan automatiskt integreras för att komplettera patientrapporterad data.")
    # Add template selection dropdown
    # List of available devices
    devices = [
        "Protes 1: Hylsa - 3D-tryckt, Fot - Sach, Suspension - Hylsa + passiv vakuum, Knä - Non-MPK",
        "Protes 2: Hylsa - DS, Fot - Trias, Suspension - Aktiv vakuum, Knä - MPK",
        "Lägg till hjälpmedel"
    ]

    # Dropdown for selecting the device
    device_choice = st.selectbox(
        "Vilken hjälpmedel vill du se?",
        devices
    )

    # Checkbox to mark the selected device as active
    active_device = st.checkbox(f"Markera {device_choice} som aktivt hjälpmedel")

    # Display selected device and mark it as active if the checkbox is checked
    if active_device:
        st.markdown(f"**Aktivt hjälpmedel:** {device_choice} 🔵")
    else:
        st.write(f"Valt hjälpmedel: {device_choice}")

    # Optionally, you can color the active device differently
    if active_device:
        # Highlight the selected active device with Streamlit's markdown
        st.markdown(f"<h3 style='color: blue;'>Aktivt hjälpmedel: {device_choice} 🔵</h3>", unsafe_allow_html=True)
    else:
        st.write(f"Valt hjälpmedel: {device_choice}")
    if device_choice == "Protes 1: Hylsa - 3D-tryckt, Fot - Sach, Suspension - Hylsa + passiv vakuum, Knä - Non-MPK":

        # Set up the seed for reproducibility (optional)
        np.random.seed(42)

        # Define the timepoints
        timepoints = ['2 weeks', '3 months', '6 months', '1 year']

        # Define the ranges or possible values for the variables
        life_quality_range = ['1', '2', '3', '4', '5', '6', '7', '8']
        mobility_levels = ['1', '2']
        satisfaction_levels = ['1', '2', '3', '4', '5']
        confort_level = ['1', '2', '3', '4', '5']
        daily_usage = ['1-3 timmar', '4-7 timmar', '+8 timmar']
        satisfaction_with_cosmetic = ['1', '2', '3', '4', '5']

        # Define the number of rows (patients) – in your case, just 1 patient
        num_rows_f = 1  # Only one patient

        # Create a list to hold all rows
        rows = []

        # Loop through timepoints to generate data for the single patient
        for tp in timepoints:
            row = {
                'Timepoint': tp,
                'Life Quality': np.random.choice(life_quality_range),
                'Mobility Level': np.random.choice(mobility_levels),
                'Satisfaction Level': np.random.choice(satisfaction_levels),
                'Comfort Level': np.random.choice(confort_level),
                'Daily Usage': np.random.choice(daily_usage),
                'Satisfaction with Cosmetic': np.random.choice(satisfaction_with_cosmetic),
            }
            rows.append(row)

        # Create DataFrame
        df = pd.DataFrame(rows)

        # Display the DataFrame
        df

        # Add template selection dropdown
        vizualization_choice = st.selectbox(
        "Vilken variabel över tid vill du se förändringar i?",
        [
            "Livskvalitet",

             "Rörelsenivå",

             "Nöjdhetsnivå",

             "Komfortnivå",

             "Daglig användning",

             "Nöjdhet med kosmetik"
          ]
          )

        # Convert categorical variables to appropriate types (if needed)
        df['Timepoint'] = pd.Categorical(df['Timepoint'], categories=timepoints, ordered=True)
        df['Life Quality'] = pd.Categorical(df['Life Quality'], categories=life_quality_range, ordered=True)
        df['Mobility Level'] = pd.Categorical(df['Mobility Level'], categories=mobility_levels, ordered=True)
        df['Satisfaction Level'] = pd.Categorical(df['Satisfaction Level'], categories=satisfaction_levels, ordered=True)
        df['Comfort Level'] = pd.Categorical(df['Comfort Level'], categories=confort_level, ordered=True)
        df['Daily Usage'] = pd.Categorical(df['Daily Usage'], categories=daily_usage, ordered=True)
        df['Satisfaction with Cosmetic'] = pd.Categorical(df['Satisfaction with Cosmetic'], categories=satisfaction_with_cosmetic, ordered=True)

        if vizualization_choice == "Livskvalitet":
            # 1. Line plot for Life Quality over Time
            plt.figure(figsize=(10, 6))
            sns.lineplot(x='Timepoint', y='Life Quality', data=df, marker='o', palette='Set1')
            plt.title('Life Quality Over Time')
            plt.xlabel('Timepoint')
            plt.ylabel('Life Quality')
            plt.xticks(rotation=45)

            # Set y-ticks to show the full range of Life Quality values from top to bottom
            plt.yticks(np.arange(0, 8, 1), life_quality_range)  # Adjusted np.arange(0, 8, 1) for 8 labels
            plt.gca().invert_yaxis()  # Optional, to have higher values at the top
            st.pyplot(plt)  # Display the plot using Streamlit

        if vizualization_choice == "Rörelsenivå":
        # 2. Line plot for Mobility Level over Time
            plt.figure(figsize=(10, 6))
            sns.lineplot(x='Timepoint', y='Mobility Level', data=df, marker='o', palette='Set2')
            plt.title('Mobility Level Over Time')
            plt.xlabel('Timepoint')
            plt.ylabel('Mobility Level')
            plt.xticks(rotation=45)

            # Set y-ticks to show the full range of Mobility Levels from top to bottom
            plt.yticks(np.arange(0, 2, 1), mobility_levels)  # Adjusted np.arange(0, 2, 1) for 2 labels
            plt.gca().invert_yaxis()  # Optional, to have higher values at the top
            st.pyplot(plt)  # Display the plot using Streamlit

        if vizualization_choice == "Nöjdhetsnivå":
            # 3. Line plot for Satisfaction Level over Time
            plt.figure(figsize=(10, 6))
            sns.lineplot(x='Timepoint', y='Satisfaction Level', data=df, marker='o', palette='Set3')
            plt.title('Satisfaction Level Over Time')
            plt.xlabel('Timepoint')
            plt.ylabel('Satisfaction Level')
            plt.xticks(rotation=45)

            # Set y-ticks to show the full range of Satisfaction Levels from top to bottom
            plt.yticks(np.arange(0, 5, 1), satisfaction_levels)  # Adjusted np.arange(0, 5, 1) for 5 labels
            plt.gca().invert_yaxis()  # Optional, to have higher values at the top
            st.pyplot(plt)  # Display the plot using Streamlit

        if vizualization_choice == "Komfortnivå":
            # 4. Bar plot for Comfort Level over Time
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Timepoint', y='Comfort Level', data=df, palette='Set1')
            plt.title('Comfort Level Over Time')
            plt.xlabel('Timepoint')
            plt.ylabel('Comfort Level')
            plt.xticks(rotation=45)

            # Set y-ticks to show the full range of Comfort Levels from top to bottom
            plt.yticks(np.arange(0, 5, 1), confort_level)  # Adjusted np.arange(0, 5, 1) for 5 labels
            plt.gca().invert_yaxis()  # Optional, to have higher values at the top
            st.pyplot(plt)  # Display the plot using Streamlit

        if vizualization_choice == "Daglig användning":
            # 5. Bar plot for Daily Usage over Time
            plt.figure(figsize=(10, 6))
            sns.countplot(x='Timepoint', hue='Daily Usage', data=df, palette='Set2')
            plt.title('Daily Usage Over Time')
            plt.xlabel('Timepoint')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            st.pyplot(plt)  # Display the plot using Streamlit

        if vizualization_choice == "Nöjdhet med kosmetik":
            # 6. Satisfaction with Cosmetic Over Time (Bar Plot)
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Timepoint', y='Satisfaction with Cosmetic', data=df, palette='Set3')
            plt.title('Satisfaction with Cosmetic Over Time')
            plt.xlabel('Timepoint')
            plt.ylabel('Satisfaction with Cosmetic')
            plt.xticks(rotation=45)

            # Set y-ticks to show the full range of Satisfaction with Cosmetic values from top to bottom
            plt.yticks(np.arange(0, 5, 1), satisfaction_with_cosmetic)  # Adjusted np.arange(0, 6, 1) for 6 labels
            plt.gca().invert_yaxis()  # Optional, to have higher values at the top
            st.pyplot(plt)  # Display the plot using Streamlit

    if device_choice == "Protes 2: Hylsa - DS, Fot - Trias, Suspension - Aktiv vakuum, Knä - MPK":
        # Set up the seed for reproducibility (optional)
        np.random.seed(7)

        # Define the timepoints
        timepoints = ['2 weeks', '3 months', '6 months', '1 year']

        # Define the ranges or possible values for the variables
        life_quality_range = ['1', '2', '3', '4', '5', '6', '7', '8']
        mobility_levels = ['3', '4']
        satisfaction_levels = ['1', '2', '3', '4', '5']
        confort_level = ['1', '2', '3', '4', '5']
        daily_usage = ['1-3 timmar', '4-7 timmar', '+8 timmar']
        satisfaction_with_cosmetic = ['1', '2', '3', '4', '5']

        # Define the number of rows (patients) – in your case, just 1 patient
        num_rows_f = 1  # Only one patient

        # Create a list to hold all rows
        rows = []

        # Loop through timepoints to generate data for the single patient
        for tp in timepoints:
            row = {
                'Timepoint': tp,
                'Life Quality': np.random.choice(life_quality_range),
                'Mobility Level': np.random.choice(mobility_levels),
                'Satisfaction Level': np.random.choice(satisfaction_levels),
                'Comfort Level': np.random.choice(confort_level),
                'Daily Usage': np.random.choice(daily_usage),
                'Satisfaction with Cosmetic': np.random.choice(satisfaction_with_cosmetic),
            }
            rows.append(row)

        # Create DataFrame
        df = pd.DataFrame(rows)

        # Display the DataFrame
        df

        # Add template selection dropdown
        vizualization_choice = st.selectbox(
        "Vilken variabel över tid vill du se förändringar i?",
        [
            "Livskvalitet",

             "Rörelsenivå",

             "Nöjdhetsnivå",

             "Komfortnivå",

             "Daglig användning",

             "Nöjdhet med kosmetik"
          ]
          )

        # Convert categorical variables to appropriate types (if needed)
        df['Timepoint'] = pd.Categorical(df['Timepoint'], categories=timepoints, ordered=True)
        df['Life Quality'] = pd.Categorical(df['Life Quality'], categories=life_quality_range, ordered=True)
        df['Mobility Level'] = pd.Categorical(df['Mobility Level'], categories=mobility_levels, ordered=True)
        df['Satisfaction Level'] = pd.Categorical(df['Satisfaction Level'], categories=satisfaction_levels, ordered=True)
        df['Comfort Level'] = pd.Categorical(df['Comfort Level'], categories=confort_level, ordered=True)
        df['Daily Usage'] = pd.Categorical(df['Daily Usage'], categories=daily_usage, ordered=True)
        df['Satisfaction with Cosmetic'] = pd.Categorical(df['Satisfaction with Cosmetic'], categories=satisfaction_with_cosmetic, ordered=True)

        if vizualization_choice == "Livskvalitet":
            # 1. Line plot for Life Quality over Time
            plt.figure(figsize=(10, 6))
            sns.lineplot(x='Timepoint', y='Life Quality', data=df, marker='o', palette='Set1')
            plt.title('Life Quality Over Time')
            plt.xlabel('Timepoint')
            plt.ylabel('Life Quality')
            plt.xticks(rotation=45)

            # Set y-ticks to show the full range of Life Quality values from top to bottom
            plt.yticks(np.arange(0, 8, 1), life_quality_range)  # Adjusted np.arange(0, 8, 1) for 8 labels
            plt.gca().invert_yaxis()  # Optional, to have higher values at the top
            st.pyplot(plt)  # Display the plot using Streamlit

        if vizualization_choice == "Rörelsenivå":
        # 2. Line plot for Mobility Level over Time
            plt.figure(figsize=(10, 6))
            sns.lineplot(x='Timepoint', y='Mobility Level', data=df, marker='o', palette='Set2')
            plt.title('Mobility Level Over Time')
            plt.xlabel('Timepoint')
            plt.ylabel('Mobility Level')
            plt.xticks(rotation=45)

            # Set y-ticks to show the full range of Mobility Levels from top to bottom
            plt.yticks(np.arange(0, 2, 1), mobility_levels)  # Adjusted np.arange(0, 2, 1) for 2 labels
            plt.gca().invert_yaxis()  # Optional, to have higher values at the top
            st.pyplot(plt)  # Display the plot using Streamlit

        if vizualization_choice == "Nöjdhetsnivå":
            # 3. Line plot for Satisfaction Level over Time
            plt.figure(figsize=(10, 6))
            sns.lineplot(x='Timepoint', y='Satisfaction Level', data=df, marker='o', palette='Set3')
            plt.title('Satisfaction Level Over Time')
            plt.xlabel('Timepoint')
            plt.ylabel('Satisfaction Level')
            plt.xticks(rotation=45)

            # Set y-ticks to show the full range of Satisfaction Levels from top to bottom
            plt.yticks(np.arange(0, 5, 1), satisfaction_levels)  # Adjusted np.arange(0, 5, 1) for 5 labels
            plt.gca().invert_yaxis()  # Optional, to have higher values at the top
            st.pyplot(plt)  # Display the plot using Streamlit

        if vizualization_choice == "Komfortnivå":
            # 4. Bar plot for Comfort Level over Time
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Timepoint', y='Comfort Level', data=df, palette='Set1')
            plt.title('Comfort Level Over Time')
            plt.xlabel('Timepoint')
            plt.ylabel('Comfort Level')
            plt.xticks(rotation=45)

            # Set y-ticks to show the full range of Comfort Levels from top to bottom
            plt.yticks(np.arange(0, 5, 1), confort_level)  # Adjusted np.arange(0, 5, 1) for 5 labels
            plt.gca().invert_yaxis()  # Optional, to have higher values at the top
            st.pyplot(plt)  # Display the plot using Streamlit

        if vizualization_choice == "Daglig användning":
            # 5. Bar plot for Daily Usage over Time
            plt.figure(figsize=(10, 6))
            sns.countplot(x='Timepoint', hue='Daily Usage', data=df, palette='Set2')
            plt.title('Daily Usage Over Time')
            plt.xlabel('Timepoint')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            st.pyplot(plt)  # Display the plot using Streamlit

        if vizualization_choice == "Nöjdhet med kosmetik":
            # 6. Satisfaction with Cosmetic Over Time (Bar Plot)
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Timepoint', y='Satisfaction with Cosmetic', data=df, palette='Set3')
            plt.title('Satisfaction with Cosmetic Over Time')
            plt.xlabel('Timepoint')
            plt.ylabel('Satisfaction with Cosmetic')
            plt.xticks(rotation=45)

            # Set y-ticks to show the full range of Satisfaction with Cosmetic values from top to bottom
            plt.yticks(np.arange(0, 5, 1), satisfaction_with_cosmetic)  # Adjusted np.arange(0, 6, 1) for 6 labels
            plt.gca().invert_yaxis()  # Optional, to have higher values at the top
            st.pyplot(plt)  # Display the plot using Streamlit

    if device_choice == "Lägg till hjälpmedel":
        st.write("Du kommer nu att sätta upp en ny additiv enhet. Vänligen välj de olika komponenttyperna som ska ställas in som bas för den additiva enheten och som kommer att utgöra basen för de data vi får om den och som kommer att användas för analys.")
        
        socket_types = {1: "3D-printad", 2: "Direct socket", 3: "Laminerad"}
        socket_f = st.radio("Vänligen välj:", options=list(socket_types.values()))

        suspension_types = {1: "sleeve + passiv vakuum", 2: "Aktiv vakuum", 3: "Pin"}
        suspension_f = st.radio("Vänligen välj:", options=list(suspension_types.values()))

        feet_types = {1: "Sach", 2: "trias", 3: "taleo"}
        feet_f = st.radio("Vänligen välj:", options=list(feet_types.values()))

        st.write(f"Du har skapat en transtibialprotes med följande komponenter:\n")
        st.write(f"{socket_f}.\n")
        st.write(f"{suspension_f}.\n")
        st.write(f"{feet_f}.\n")
        st.write("De kommande uppgifterna kommer automatiskt att associeras med denna enhet.\n")
        st.write("Om du vill ändra det, välj ett annat alternativ för den enhet som patienten faktiskt använder (den enhet som patienten säger att han/hon använder i det dagliga livet).\n")

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