import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle



# Set up the page configuration
st.set_page_config(page_title="Klinisk Dokumentation Dashboard")

# Sidebar - Language Selection
language = st.sidebar.selectbox("Välj språk / Select language", ["Svenska", "English"])

# Text based on selected language
if language == "Svenska":
    st.title("Välkommen till prototypen för Klinisk Dokumentation!")
    st.write("Utforska sätt att optimera klinisk dokumentation för att spara tid för kliniker.")
    st.write("Utforska hur journalföring kan optimeras för att spara tid för kliniker.")
    st.write("Utforska hur Patientrapporterade Resultatmått (PROMs) kan inkluderas i behandlingsresan för att skapa en grund för evidensbaserad vård!")

    # Sidebar - Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Välj en sida:", ["Journal automatisering", "PROM Data - Svenska", "Analyserbara Insikter"])

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
            walking_speed = 0
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

    elif page == "PROM Data - Svenska":
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
    

else:  # English version
    st.title("Welcome to the LLCW enhancement dashblard")
    st.write("Explore ways to optimize clinical documentation to save time, based on journal templates requested by clinicians.")
    st.write("Explore which patient reported data clincins find useful to be collected")
    st.write("Explore how interoperability efforts can be automated")

    # Sidebar - Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", ["Journal Automation", "PROM Data - English", "Actionable Insights"])

    if page == "Journal Automation":
        st.title("Journal Automation")

        # Add template selection dropdown
        template_choice = st.selectbox(
            "Choose the template you want to use:",
            [
                "Initial Assessment After Upper Limb Amputation",
                "Prosthesis Adjustment for Lower Limb",
                "Lower Limb Prosthesis Delivery"
            ]
        )

        # Template 1: Initial Assessment After Upper Limb Amputation
        if template_choice == "Initial Assessment After Upper Limb Amputation":
            st.title("Initial Assessment After Upper Limb Amputation")
            st.write("Welcome to the page for Initial Assessment!")
            st.write("Select multiple options to create a clinical note (for instance, in this case, the first assessment after upper limb amputation).")
            st.write("The clinical note will be generated without the clinician needing to type everything manually, covering key aspects that are usually discussed. The clinician can then review and make changes if needed.")
            st.write("In the background each option is mapped to internationally accepted medical terminology standards (ICD-10 for diagnosis and SNOMED CT for treatment) making the process automatic")

            # Define and display input options for amputation type, place, cognition, etc.
            amputation_types_dict = {1: "Traumatic", 2: "Congenital"}
            st.write("### Amputation Type")
            amputation_type = st.radio("Please select the amputation type:", options=list(amputation_types_dict.values()))

            place_dict = {1: "Clinic", 2: "Hospital"}
            st.write("### Meeting Place")
            meeting_place = st.radio("Please select meeting place:", options=list(place_dict.values()))

            cognition_dict = {1: "Good cognition", 2: "Poor cognition"}
            st.write("### Cognitive Level")
            cognitive_level = st.radio("Please select cognitive level:", options=list(cognition_dict.values()))

            prosthesis_interest_dict = {1: "Positive", 2: "Negative"}
            st.write("### Interest in Prosthesis")
            prosthesis_interest = st.radio("Please select your interest in prosthesis:", options=list(prosthesis_interest_dict.values()))

            side_dict = {
                1: "Amputation of right upper extremity", 
                2: "Amputation of left upper extremity", 
                3: "Bilateral amputation of upper limbs", 
                4: "Amputation of both arms through humerus", 
                5: "Amputation of both forearms through radius and ulna", 
                6: "Amputation of both hands"
            }
            st.write("### Amputation Side")
            amputation_side = st.radio("Please select amputation side:", options=list(side_dict.values()))

            level_dict = {
                1: "Shoulder disarticulation", 
                2: "Transhumeral amputation", 
                3: "Transradial amputation", 
                4: "Partial hand amputation", 
                5: "Complete hand amputation"
            }
            st.write("### Amputation Level")
            amputation_level = st.radio("Please select amputation level:", options=list(level_dict.values()))

            # Function to display and get patient assessment responses
            def get_patient_assessment(assessment_name):
                valid_range = ("Yes", "No")
                st.write(f"### {assessment_name}")
                assessment_value = st.radio(f"Is the patient {assessment_name.lower()}?", options=valid_range)
                if assessment_value == "Yes":
                    st.write(f"The patient reports that they often use assistive devices in daily life.")
                elif assessment_value == "No":
                    st.write(f"The patient reports that they do not use assistive devices in daily life.")
                return assessment_value

            assessments_list = [
                "Independent with dressing",
                "Independent at meals",
                "Independent with personal care",
                "Ability to perform personal hygiene",
                "Uses assistive devices in daily life",
                "Fit for work",
                "Ability to engage in a hobby",
                "Ability to perform creative activity",
                "Ability to perform gardening tasks",
                "Ability to participate in play and sports activities",
                "Ability to use public recreational facilities"
            ]

            assessment_answers = []
            for assessment_name in assessments_list:
                response = get_patient_assessment(assessment_name)
                assessment_answers.append((assessment_name, response))

            # Button to generate clinical note
            if st.button("Generate Clinical Note"):
                clinical_note = ""  # Reset the note for a new generation

                # Append patient's first post-amputation visit information
                clinical_note += f"Met with patient with {amputation_level} at {meeting_place} for the first visit after amputation.\n"
                clinical_note += f"Patient has a {amputation_side} of {amputation_types_dict[1]} etiology.\n"

                # Append prior reports from the assessment
                clinical_note += "Asked the patient about their abilities prior to the amputation, and they report:\n"
                for report in assessment_answers:
                    clinical_note += f"- {report[0]}: {report[1]}\n"

                # Append cognition and interest in prosthesis
                cognition_mapping = {
                    "Good cognition": 1,
                    "Poor cognition": 2
                }

                # Match the selected interest value to the correct dictionary key
                prosthesis_interest_mapping = {
                    "Positive": 1,
                    "Negative": 2
                }
                clinical_note += f"Patient appears to have {cognition_dict[cognition_mapping[cognitive_level]]} and an understanding of the situation. When asked about prosthesis, the patient shows {prosthesis_interest_dict[prosthesis_interest_mapping[prosthesis_interest]]} interest.\n"

                # Append final follow-up statement
                clinical_note += "Follow-up is scheduled to discuss next steps."

                # Display the clinical note directly
                st.text_area("Clinical Notes:", clinical_note, height=300)

        # Template 2: Prosthesis Adjustment for Lower Limb
        elif template_choice == "Prosthesis Adjustment for Lower Limb":
            st.title("Prosthesis Adjustment for Lower Limb")
            st.write("Select multiple options to create a clinical note.")
            st.write("The most common reasons for adjustment are listed, with the possibility of making additional selections based on the chosen option to create a complete clinical note.")
            st.write("Depending on the main reasons for the visit, CPOs will be able to write down what they did, which is easily implemented in the note.")
            st.write("Manually typed entries can be followed based on frequency of use so they can then be added as multiple choice")

            # Define reasons for adjustment
            adjustment_reasons = {
                    1: "Needs new component (liner)",
                    2: "Needs new component (sleeve)",
                    3: "Discomfort during use",
                    4: "Changed stump volume",
                    5: "Poor fit",
                    6: "Other reason"
                }

            st.write("### Reason for Visit")
            selected_reason = st.radio("Please select the reason for the visit:", options=list(adjustment_reasons.values()))

            reason_1 = [selected_reason]

            # Handle different reason categories with sub-options
            if selected_reason == "Discomfort during use":
                    discomfort_reasons = {
                        1: "Pain around the fibula head",
                        2: "Pain at the distal end of the tibia",
                        3: "Pain under the stump",
                        4: "Pressure sensation during specific loading",
                        5: "General tenderness or irritation in the sleeve"
                    }
                    discomfort_reason = st.selectbox("Select reason for discomfort:", list(discomfort_reasons.values()))
                    reason_2 = [discomfort_reason]
                    treatment_steps = st.text_input("Please write the steps you took during the visit to solve the patient's issue:")

            if selected_reason == "Other reason":
                    visit_reason = st.text_input("Please describe the reason for the visit:")
                    treatment_steps_2 = st.text_input("Please write the steps you took during the visit to solve the patient's issue:")

            if selected_reason == "Changed stump volume" or selected_reason == "Poor fit":
                    fixable_options = {
                        1: "Can be solved during the visit (without creating a new sleeve)",
                        2: "Cannot be solved during the visit (new sleeve needs to be made)"
                    }
                    fix_option = st.selectbox("Select what was done during the visit:", list(fixable_options.values()))
                    reason_3 = [fix_option]

            if selected_reason == "Needs new component (liner)" or selected_reason == "Needs new component (sleeve)":
                    stock_options = {
                        1: "Had the component the patient needed in stock (delivered immediately)",
                        2: "Did not have the component in stock (will be ordered and delivered when it arrives)"
                    }
                    stock_answer = st.selectbox("Select if the component was in stock:", list(stock_options.values()))
                    stock_f = [stock_answer]

                # Define visit outcomes
            visit_outcomes = {
                    1: "Solved the patient's issue (the patient will contact us if needed)",
                    2: "Could not solve the patient's issue. Discussed next steps and scheduled follow-up"
                }
            st.write("### Outcome of the Visit")
            outcome_answer = st.radio("Please select the outcome of the visit:", options=list(visit_outcomes.values()))
            outcome_1 = [outcome_answer]

            # Button to generate clinical note
            if st.button("Generate Clinical Notes"):
                    clinical_note = ""  # Reset the note for a new generation

                    # Append adjustment visit information
                    if reason_1[0] != "Other reason":
                        clinical_note += f"The patient visits us for prosthesis adjustment and reports {reason_1[0]}.\n"
                    else:
                        clinical_note += f"The patient visits us for prosthesis adjustment and reports {visit_reason}.\n"

                    if reason_1[0] == "Discomfort during use":
                        clinical_note += f"Upon examination, the patient reports {reason_2[0]} during walking.\n"
                        clinical_note += f"During the visit, the following steps were taken to adjust the patient's prosthesis:\n"
                        clinical_note += f"{treatment_steps}.\n"
                    if reason_1[0] == "Other reason":
                        clinical_note += f"During the visit, the following steps were taken to adjust the patient's prosthesis:\n"
                        clinical_note += f"{treatment_steps_2}.\n"
                    elif reason_1[0] == "Changed stump volume" or reason_1[0] == "Poor fit":
                        clinical_note += f"During the visit, it was assessed that {reason_3[0]}.\n"
                    elif reason_1[0] == "Needs new component (sleeve)" or reason_1[0] == "Needs new component (liner)":
                        clinical_note += f"During the visit, {stock_f[0]}.\n"
                    if outcome_1[0] == "Solved the patient's issue (the patient will contact us if needed)":
                        clinical_note += f"At the end of the visit: {outcome_1[0]}.\n"
                    else:
                        clinical_note += f"At the end of the visit: {outcome_1[0]}.\n"

                    # Display the clinical note directly
                    st.text_area("Clinical Notes:", clinical_note, height=300)
        
        elif template_choice == "Lower Limb Prosthesis Delivery":
                st.title("Lower Limb Prosthesis Delivery")
                st.write("Select multiple options to create a clinical note.")
                st.write("Generate clinical notes with the option for clinicians to input relevant treatment information (patient-reported and functional tests) and receive automatic insights.")
                st.write("Connections to previous clinical notes can be created to better automate the process. For example, K-level can be automatically assessed from an initial assessment template and later linked to the delivery template.")

                # Socket fit
                fit = {1: "Good fit", 2: "Bad fit"}
                st.write("### How was the socket fit?")
                answer_fit = st.radio("Please select:", options=list(fit.values()))

                if answer_fit == "Bad fit":
                    compensation = {1: "Tried with 1 prosthetic sock and it got better",
                                    2: "Tried with 2 prosthetic socks and it got better",
                                    3: "Tried with 3 prosthetic socks and it got better"}
                    answer_compensation = st.radio("Select solution:", options=list(compensation.values()))

                # Ability to don and doff prosthesis
                donning_ability = {
                    1: "Can do",
                    2: "Cannot do",
                    3: "Can do but needs assistance"
                }

                st.write("### Ability to don the prosthesis independently.")
                answer_don = st.radio("Please select:", options=list(donning_ability.values()))

                # Handle assistance requirement
                if answer_don == "Can do but needs assistance" or answer_don == "Cannot do":
                    assistance = {
                        1: "Reports receiving assistance at home from someone who can assist",
                        2: "Reports being unable to receive assistance at home"
                    }
                    answer_assistance = st.radio("Please select assistance need:", options=list(assistance.values()))

                # Patient post-delivery assessment
                def get_patient_post_delivery_assessment(assessment_name):
                    valid_range = ("Yes", "No")
                    st.write(f"### {assessment_name}")
                    assessment_value = st.radio(f"Is the patient {assessment_name.lower()}?", options=valid_range)
                    return assessment_value

                assessments = [
                    "Ability to transfer from chair to bed",
                    "Ability to walk with prosthesis",
                    "Ability to sit up without support",
                    "Ability to manage stairs",
                    "Ability to walk on uneven surfaces",
                    "Ability to participate in sports activities",
                    "Ability to manage pain and discomfort from prosthesis",
                    "Ability to perform a wheelchair transfer",
                ]

                Answers_7 = []
                for assessment_name in assessments:
                    response = get_patient_post_delivery_assessment(assessment_name)
                    Answers_7.append((assessment_name, response))

                # Functional tests
                performed = {1: "Yes", 2: "No"}
                st.write("### Has the patient completed the *Time Up and Go Test*?")
                answer_tug = st.radio("Please select:", options=list(performed.values()), key="tug_test")
                if answer_tug == "Yes":
                    TUG = st.text_input("Please enter how long it took the patient to complete the test in seconds. For example, if it took 1 minute 30 seconds, enter 90).", key="tug_input")
                    TUG_NUMBER = int(TUG) if TUG.isdigit() else 0  # Safe conversion

                st.write("### Has the patient completed the *Four Square Step Test*?")
                answer_four_sq = st.radio("Please select:", options=list(performed.values()), key="four_square_test")
                if answer_four_sq == "Yes":
                    four_sq = st.text_input("Please enter how long it took the patient to complete the test in seconds. For example, if it took 1 minute 30 seconds, enter 90).", key="four_sq_input")
                    four_sq_f = int(four_sq) if four_sq.isdigit() else 0  # Safe conversion

                st.write("### Has the patient completed the *100 Meter Walk Test*?")
                answer_100_test = st.radio("Please select:", options=list(performed.values()), key="100_test")
                walking_speed_2 = 0
                if answer_100_test == "Yes":
                    meter_100 = st.text_input("Please enter how long it took the patient to complete the test in seconds. For example, if it took 1 minute 30 seconds, enter 90).", key="100_test_input")
                    METER_100 = int(meter_100) if meter_100.isdigit() else 0  # Safe conversion
                    if METER_100 > 0:
                        walking_speed_2 = 100 / METER_100

                # Rehabilitation
                rehab_interest = {1: "Interested", 2: "Not interested"}
                st.write("Is the patient interested in rehabilitation?")
                rehab_interest_selected = st.radio("Please select:", options=list(rehab_interest.values()))

                # Handle rehabilitation needs
                if rehab_interest_selected == "Interested":
                    rehabilitation_options = {
                        1: "Wants to join a walking school",
                        2: "Reports having access to private physiotherapy",
                        3: "Wants individual sessions with a physiotherapist"
                    }
                    answer_rehab_assistance = st.radio("Please select rehabilitation need:", options=list(rehabilitation_options.values()))

                # Button to generate clinical note
                if st.button("Generate Clinical Notes"):
                    clinical_note = ""  # Reset the note for a new generation

                    # Append delivery visit information
                    clinical_note += f"The patient visits us for prosthesis delivery.\n"
                    clinical_note += f"During the fitting, the socket was checked. The socket fit is {answer_fit}, which the patient agrees with.\n"
                    if answer_fit == "Bad fit":
                        clinical_note += f"To improve the fit, {answer_compensation}.\n"
                    clinical_note += f"Showed the patient how to don the prosthesis and checked if they can do it independently, which they {answer_don}.\n"
                    if answer_don == "Cannot do" or answer_don == "Can do but needs assistance":
                        clinical_note += f"Asked the patient and they {answer_assistance}, and they should practice to be able to manage on their own.\n"
                    clinical_note += "During the visit, the patient was assessed on the following activities:\n"
                    for report in Answers_7:
                        clinical_note += f"- {report[0]}: {report[1]}\n"
                    if answer_100_test == "Yes":
                        clinical_note += f"The patient completed the 100-meter walking test in {METER_100} seconds.\n"
                        clinical_note += f"The patient's walking speed is {walking_speed_2:.2f} meters per second.\n"
                    if answer_tug == "Yes":
                        clinical_note += f"The patient completed the TUG test in {TUG_NUMBER} seconds.\n"
                        if TUG_NUMBER > 30:
                            clinical_note += "Based on the TUG performance, the patient is classified as K-level: 1 - Limited mobility, requires assistive devices or assistance.\n"
                        elif 20 <= TUG_NUMBER <= 30:
                            clinical_note += "Based on the TUG performance, the patient is classified as K-level: 2 - Limited community mobility.\n"
                        elif 15 <= TUG_NUMBER < 20:
                            clinical_note += "Based on the TUG performance, the patient is classified as K-level: 3 - Community mobility with varying speeds.\n"
                        else:
                            clinical_note += "Based on the TUG performance, the patient is classified as K-level: 4 - High mobility, capable of recreation or competition.\n"
                    if answer_four_sq == "Yes":
                        clinical_note += f"The patient completed the Four Square Step Test in {four_sq_f} seconds.\n"
                        if four_sq_f > 30:
                            clinical_note += ("Based on the Four Square Step Test performance, the fall risk is classified as high. "
                                            "Further evaluation for fall prevention measures is recommended.\n")
                        elif 20 <= four_sq_f <= 30:
                            clinical_note += ("Based on the Four Square Step Test performance, the fall risk is considered moderate. "
                                            "Consider adjustments for increased balance and safety.\n")
                        elif 15 <= four_sq_f < 20:
                            clinical_note += ("Based on the Four Square Step Test performance, the fall risk is considered low. "
                                            "Continued monitoring is recommended.\n")
                        else:
                            clinical_note += ("Based on the Four Square Step Test performance, the fall risk is considered very low. "
                                            "The patient shows good balance and stability.\n")

                    if rehab_interest_selected == "Interested":
                        clinical_note += f"Asked the patient about rehabilitation, and they are {rehab_interest_selected} and {answer_rehab_assistance}.\n"
                    else:
                        clinical_note += f"Asked the patient about rehabilitation, and they are {rehab_interest_selected[0]}.\n"
                    clinical_note += "Agreed with the patient that they should try to use the prosthesis as much as possible and contact us if needed.\n"

                    # Display the clinical note directly
                    st.text_area("Clinical Notes:", clinical_note, height=300)
    elif page == "PROM Data - English":
        st.title("Example of PROM-based Data")
        st.write("Welcome to the PROM data page!")
        st.write("List of main patient reported data CPOs consider would be useful for tracking patients outcomes.")
        st.write("This enables quantification of treatment effects and understanding of how component changes (e.g., a new prosthetic knee joint) affect the patient's well-being.")
        st.write("This will help better justify the prescribing of components and obtaining approval for more expensive options.")
        st.write("Recommendation to link information is to specific devices so it is easy for CPOs to understand the results of each device/component change in overall well-being.")
        st.write("In the future, triggers can be added (requested by CPOs) to automatically inform clinicians of patient needs (e.g., if the comfort level drops below a certain threshold, clinicians will receive a reminder to potentially contact the patient for socket manufacturing).")
        st.write("Data from the patient record (such as performing specific functional tests) that is entered into the record can be automatically integrated to complement patient-reported data.")

        # Add template selection dropdown
        # List of available devices
        devices = [
            "Prosthesis 1: Socket - 3D printed, Foot - Sach, Suspension - Socket + passive vacuum, Knee - Non-MPK",
            "Prosthesis 2: Socket - DS, Foot - Trias, Suspension - Active vacuum, Knee - MPK",
            "Add device"
        ]

        # Dropdown for selecting the device
        device_choice = st.selectbox(
            "Which device would you like to view?",
            devices
        )

        # Checkbox to mark the selected device as active
        active_device = st.checkbox(f"Mark {device_choice} as active device")

        # Display selected device and mark it as active if the checkbox is checked
        if active_device:
            st.markdown(f"**Active Device:** {device_choice} 🔵")
        else:
            st.write(f"Selected device: {device_choice}")

        # Optionally, you can color the active device differently
        if active_device:
            # Highlight the selected active device with Streamlit's markdown
            st.markdown(f"<h3 style='color: blue;'>Active Device: {device_choice} 🔵</h3>", unsafe_allow_html=True)
        else:
            st.write(f"Selected device: {device_choice}")
      

        if device_choice == "Prosthesis 1: Socket - 3D printed, Foot - Sach, Suspension - Socket + passive vacuum, Knee - Non-MPK":

                # Set up the seed for reproducibility (optional)
                np.random.seed(42)

                # Define the timepoints
                timepoints = ['2 weeks', '3 months', '6 months', '1 year']

                # Define the ranges or possible values for the variables
                life_quality_range = ['1', '2', '3', '4', '5', '6', '7', '8']
                mobility_levels = ['1', '2']
                satisfaction_levels = ['1', '2', '3', '4', '5']
                comfort_level = ['1', '2', '3', '4', '5']
                daily_usage = ['1-3 hours', '4-7 hours', '+8 hours']
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
                        'Comfort Level': np.random.choice(comfort_level),
                        'Daily Usage': np.random.choice(daily_usage),
                        'Satisfaction with Cosmetic': np.random.choice(satisfaction_with_cosmetic),
                    }
                    rows.append(row)

                # Create DataFrame
                df = pd.DataFrame(rows)

                # Display the DataFrame
                df

                # Add template selection dropdown
                visualization_choice = st.selectbox(
                    "Which variable would you like to see changes over time for?",
                    [
                        "Life Quality",
                        "Mobility Level",
                        "Satisfaction Level",
                        "Comfort Level",
                        "Daily Usage",
                        "Satisfaction with Cosmetic"
                    ]
                )

                # Convert categorical variables to appropriate types (if needed)
                df['Timepoint'] = pd.Categorical(df['Timepoint'], categories=timepoints, ordered=True)
                df['Life Quality'] = pd.Categorical(df['Life Quality'], categories=life_quality_range, ordered=True)
                df['Mobility Level'] = pd.Categorical(df['Mobility Level'], categories=mobility_levels, ordered=True)
                df['Satisfaction Level'] = pd.Categorical(df['Satisfaction Level'], categories=satisfaction_levels, ordered=True)
                df['Comfort Level'] = pd.Categorical(df['Comfort Level'], categories=comfort_level, ordered=True)
                df['Daily Usage'] = pd.Categorical(df['Daily Usage'], categories=daily_usage, ordered=True)
                df['Satisfaction with Cosmetic'] = pd.Categorical(df['Satisfaction with Cosmetic'], categories=satisfaction_with_cosmetic, ordered=True)

                if visualization_choice == "Life Quality":
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

                if visualization_choice == "Mobility Level":
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

                if visualization_choice == "Satisfaction Level":
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

                if visualization_choice == "Comfort Level":
                    # 4. Bar plot for Comfort Level over Time
                    plt.figure(figsize=(10, 6))
                    sns.barplot(x='Timepoint', y='Comfort Level', data=df, palette='Set1')
                    plt.title('Comfort Level Over Time')
                    plt.xlabel('Timepoint')
                    plt.ylabel('Comfort Level')
                    plt.xticks(rotation=45)

                    # Set y-ticks to show the full range of Comfort Levels from top to bottom
                    plt.yticks(np.arange(0, 5, 1), comfort_level)  # Adjusted np.arange(0, 5, 1) for 5 labels
                    plt.gca().invert_yaxis()  # Optional, to have higher values at the top
                    st.pyplot(plt)  # Display the plot using Streamlit

                if visualization_choice == "Daily Usage":
                    # 5. Bar plot for Daily Usage over Time
                    plt.figure(figsize=(10, 6))
                    sns.countplot(x='Timepoint', hue='Daily Usage', data=df, palette='Set2')
                    plt.title('Daily Usage Over Time')
                    plt.xlabel('Timepoint')
                    plt.ylabel('Count')
                    plt.xticks(rotation=45)
                    st.pyplot(plt)  # Display the plot using Streamlit

                if visualization_choice == "Satisfaction with Cosmetic":
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
        

        if device_choice == "Prosthesis 2: Socket - DS, Foot - Trias, Suspension - Active vacuum, Knee - MPK":
            # Set up the seed for reproducibility (optional)
            np.random.seed(7)

            # Define the timepoints
            timepoints = ['2 weeks', '3 months', '6 months', '1 year']

            # Define the ranges or possible values for the variables
            life_quality_range = ['1', '2', '3', '4', '5', '6', '7', '8']
            mobility_levels = ['3', '4']
            satisfaction_levels = ['1', '2', '3', '4', '5']
            comfort_level = ['1', '2', '3', '4', '5']
            daily_usage = ['1-3 hours', '4-7 hours', '+8 hours']
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
                    'Comfort Level': np.random.choice(comfort_level),
                    'Daily Usage': np.random.choice(daily_usage),
                    'Satisfaction with Cosmetic': np.random.choice(satisfaction_with_cosmetic),
                }
                rows.append(row)

            # Create DataFrame
            df = pd.DataFrame(rows)

            # Display the DataFrame
            df

            # Add template selection dropdown
            visualization_choice = st.selectbox(
                "Which variable over time would you like to see changes in?",
                [
                    "Life Quality",
                    "Mobility Level",
                    "Satisfaction Level",
                    "Comfort Level",
                    "Daily Usage",
                    "Satisfaction with Cosmetic"
                ]
            )

            # Convert categorical variables to appropriate types (if needed)
            df['Timepoint'] = pd.Categorical(df['Timepoint'], categories=timepoints, ordered=True)
            df['Life Quality'] = pd.Categorical(df['Life Quality'], categories=life_quality_range, ordered=True)
            df['Mobility Level'] = pd.Categorical(df['Mobility Level'], categories=mobility_levels, ordered=True)
            df['Satisfaction Level'] = pd.Categorical(df['Satisfaction Level'], categories=satisfaction_levels, ordered=True)
            df['Comfort Level'] = pd.Categorical(df['Comfort Level'], categories=comfort_level, ordered=True)
            df['Daily Usage'] = pd.Categorical(df['Daily Usage'], categories=daily_usage, ordered=True)
            df['Satisfaction with Cosmetic'] = pd.Categorical(df['Satisfaction with Cosmetic'], categories=satisfaction_with_cosmetic, ordered=True)

            if visualization_choice == "Life Quality":
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

            if visualization_choice == "Mobility Level":
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

            if visualization_choice == "Satisfaction Level":
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

            if visualization_choice == "Comfort Level":
                # 4. Bar plot for Comfort Level over Time
                plt.figure(figsize=(10, 6))
                sns.barplot(x='Timepoint', y='Comfort Level', data=df, palette='Set1')
                plt.title('Comfort Level Over Time')
                plt.xlabel('Timepoint')
                plt.ylabel('Comfort Level')
                plt.xticks(rotation=45)

                # Set y-ticks to show the full range of Comfort Levels from top to bottom
                plt.yticks(np.arange(0, 5, 1), comfort_level)  # Adjusted np.arange(0, 5, 1) for 5 labels
                plt.gca().invert_yaxis()  # Optional, to have higher values at the top
                st.pyplot(plt)  # Display the plot using Streamlit

            if visualization_choice == "Daily Usage":
                # 5. Bar plot for Daily Usage over Time
                plt.figure(figsize=(10, 6))
                sns.countplot(x='Timepoint', hue='Daily Usage', data=df, palette='Set2')
                plt.title('Daily Usage Over Time')
                plt.xlabel('Timepoint')
                plt.ylabel('Count')
                plt.xticks(rotation=45)
                st.pyplot(plt)  # Display the plot using Streamlit

            if visualization_choice == "Satisfaction with Cosmetic":
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

        if device_choice == "Add New Assistive Device":
            st.write("You are now setting up a new additive unit. Please select the different component types that will be set as the base for the additive unit and will form the basis for the data we collect about it, which will be used for analysis.")
            st.write("Main idea is that CPOs will add new devices in case of change and be able to set them as the active device so reported data gets attached to it.")
            
            socket_types = {1: "3D printed", 2: "Direct socket", 3: "Laminated"}
            socket_f = st.radio("Please choose:", options=list(socket_types.values()))

            suspension_types = {1: "Sleeve + passive vacuum", 2: "Active vacuum", 3: "Pin"}
            suspension_f = st.radio("Please choose:", options=list(suspension_types.values()))

            feet_types = {1: "Sach", 2: "Trias", 3: "Taleo"}
            feet_f = st.radio("Please choose:", options=list(feet_types.values()))

            st.write(f"You have created a transtibial prosthesis with the following components:\n")
            st.write(f"{socket_f}.\n")
            st.write(f"{suspension_f}.\n")
            st.write(f"{feet_f}.\n")
            st.write("The upcoming data will be automatically associated with this device.\n")
            st.write("If you want to change it, select another option for the device that the patient actually uses (the device the patient reports using in daily life).\n")
    elif page == "Actionable Insights":
        st.title("Using Data to Generate Guideline Insights")
        st.write("Welcome to the Analyzable Insights page!")
        st.write("Examples of how PROM-based data and clinical record data can be used to generate analyzable insights.")
        st.write("When clinicians use clinical templates on the first page, all options are linked to internationally accepted medical coding systems.")
        st.write("This ensures that data from all clinics can be understood regardless of language allowing knowledge exchange within Ottobock clinics.")
        st.write("From it trends from patient type/delivered device can be identified and displayed to clinician (requested by CPOs). Not necessarily as clinical decision support but as additional information.")
        st.write("For example for a new assement of TT amputee insights such as: For this patient profile the Trias foot as resulted in the best outcome for 85% patinets with similar profile, can be displayed")

        # Set up the seed for reproducibility (optional)
        np.random.seed(42)

        # Define the ranges or possible values for the variables
        Patient_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        Amputation_type = ['79733001', '265736004', '88312006', '397218006', '180030006']
        Amputation_cause = ['262595009', '205386003', '46635009', '40713004', '3947001']
        Amputation_Side = ['732213003', '732214009', '732212008']
        life_quality_range = ['1', '2', '3', '4', '5', '6', '7', '8']
        prosthesis_types = [1, 2, 3]  # Prosthesis types
        mobility_levels = ['1', '2', '3', '4']
        satisfaction_levels = ['1', '2', '3', '4']
        Prosthesis_socket = ['3D-printed', 'Direct socket', 'Conventional']
        Prosthesis_knee = ['MPK', 'non-MPK']
        Prosthesis_feet = ['Sach', 'Energy return', 'Electronic']

        # Define the number of rows for the simulated data
        num_rows = 50  # You can change this number as needed

        # Create random data for the table
        data = {
            'Life Quality': np.random.choice(life_quality_range, num_rows),
            'Prosthesis': np.random.choice(prosthesis_types, num_rows),
            'Prosthesis_socket': np.random.choice(Prosthesis_socket, num_rows),
            'Prosthesis_knee': np.random.choice(Prosthesis_knee, num_rows),
            'Prosthesis_feet': np.random.choice(Prosthesis_feet, num_rows),
            'Mobility Level': np.random.choice(mobility_levels, num_rows),
            'Satisfaction Level': np.random.choice(satisfaction_levels, num_rows),
            'Patient_id': np.random.choice(Patient_id, num_rows),
            'Amputation_type': np.random.choice(Amputation_type, num_rows),
            'Amputation_cause': np.random.choice(Amputation_cause, num_rows),
            'Amputation_Side': np.random.choice(Amputation_Side, num_rows),
        }

        # Create a DataFrame using pandas
        df = pd.DataFrame(data)

        # Display the table in the Streamlit app
        st.write("### Simulated Patient Data Table")
        st.dataframe(df)  # Display the table
        st.write("Here, information for all treated patients will be organized in a way that allows for analysis.")
        st.write("Included in the information is data from PROMs and from the use of templates, like the one on the first page, for creating clinical notes.")
        st.write("All options presented to clinicians when creating notes are linked to internationally accepted coding systems, making it easy to implement this system globally in all clinics.")
        st.write("The more clinics that use it, the more data is generated, making it possible to ensure that all patients receive the same type of care regardless of location.")
        st.write("For patterns, guidelines for care can be created, not to tell clinicians what to do, but to show them what they can expect from their choices.")
        st.write("It will be possible for clinicians to input their patient's information and see how treatment choices (such as switching knee joints) can affect multiple variables, like mobility level.")
        st.write("Documentation of expected outcomes for more expensive components will then be based on data rather than what each clinician subjectively expects.")
