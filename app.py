import streamlit as st

# -------------------------
# Load questions file
# -------------------------

def load_questions():
    questions = []
    try:
        with open("questions_and_answers.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split(";")
                if len(parts) < 6:
                    continue

                qid = parts[0]
                correct_raw = parts[1]
                question = parts[2]
                options = parts[3:]

                try:
                    correct_index = int(correct_raw) - 1
                except:
                    continue

                questions.append({
                    "question": question,
                    "options": options,
                    "correct_index": correct_index
                })
    except:
        st.error("Could not load questions file.")
    
    return questions


# -------------------------
# Streamlit App
# -------------------------

st.title("🎮 Online Reputation Management Quiz")
st.write("Welcome! Answer the questions and test your knowledge.")

questions = load_questions()

# Initialize session state
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.finished = False

# If game finished
if st.session_state.finished:
    st.success(f"Your final score: {st.session_state.score}/{len(questions)} 🎉")
    if st.button("Play again"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.finished = False
    st.stop()

# Display current question
q = questions[st.session_state.index]

st.header(f"Question {st.session_state.index + 1}/{len(questions)}")
st.write(q["question"])

choice = st.radio("Choose an answer:", q["options"])

if st.button("Submit"):
    if q["options"].index(choice) == q["correct_index"]:
        st.session_state.score += 1
        st.success("Correct! 🎉")
    else:
        correct_answer = q["options"][q["correct_index"]]
        st.error(f"Wrong ❌ The correct answer was: {correct_answer}")

    # Go to next question
    st.session_state.index += 1
    if st.session_state.index >= len(questions):
        st.session_state.finished = True

    st.experimental_rerun()
