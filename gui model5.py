
import time
import random
import os
import streamlit as st

# File to store high scores
HIGH_SCORE_FILE = "high_scores.txt"

# Predefined sentences for each difficulty level
SENTENCES = {
    "easy": [
        "I like to eat apples",
        "Python is fun to learn",
        "It is a sunny day",
        "We play football daily"
    ],
    "medium": [
        "Concurrency in Python can be tricky due to the Global Interpreter Lock.",
        "Asynchronous programming requires a good understanding of event loops.",
        "Keyboard efficiency improves dramatically with proper finger placement."
    ],
    "hard": [
        "Syntactic ambiguity occurs when a sentence can have more than one meaning",
        "Optimization of algorithms can lead to faster execution and lower memory usage",
        "Parallel computing is a type of computation in which many calculations are carried out simultaneously",
        "In data science, preprocessing is a crucial step before model training"
    ]
}
# ----------------------------------------------------------------------------------------------------------------------
# Accuracy calculation
def calculate_accuracy(original, typed):
    original_words = original.strip().split()
    typed_words = typed.strip().split()
    correct = sum(o == t for o, t in zip(original_words, typed_words))

    highlighted_output = []
    for i, word in enumerate(original_words):
        if i < len(typed_words) and typed_words[i] == word:
            highlighted_output.append(f":green[{word}]")
        else:
            wrong = typed_words[i] if i < len(typed_words) else "___"
            highlighted_output.append(f":red[{wrong}]")

    st.markdown(" ".join(highlighted_output))
    return (correct / len(original_words)) * 100 if original_words else 0

# ---------------------------------------------------------------------------------------------------------------------
# Save and show scores
def save_score(username, difficulty, score, accuracy):
    with open(HIGH_SCORE_FILE, "a") as f:
        f.write(f"{username},{difficulty},{score},{accuracy}\n")

def show_high_scores():
    st.subheader("🏆 High Scores")
    if not os.path.exists(HIGH_SCORE_FILE):
        st.info("No high scores yet.")
        return

    scores = []
    with open(HIGH_SCORE_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 4:
                name, level, score, accuracy = parts
                try:
                    scores.append((name, level, float(score), float(accuracy)))
                except ValueError:
                    continue

    if not scores:
        st.info("No valid high scores found.")
        return

    scores.sort(key=lambda x: (x[2], x[3]), reverse=True)
    for i, (name, level, score, accuracy) in enumerate(scores[:10], start=1):
        st.write(f"**{i}.** {name} - {level.capitalize()} - {score} WPM - {accuracy}%")

# ----------------------------------------------------------------------------------------------------------------------
# Typing Test
def typing_test(sentence):
    st.write("✍️ Type the following sentence:")
    st.markdown(f"> {sentence}")

    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    typed = st.text_area("Start typing here:", key="typed_text", height=150)

    if st.session_state.start_time is None and typed.strip() != "":
        st.session_state.start_time = time.time()

    if st.button("Submit"):
        if st.session_state.start_time is None:
            st.warning("You need to type something first!")
            return None, None, None

        end_time = time.time()
        elapsed_time = end_time - st.session_state.start_time
        words = typed.strip().split()
        word_count = len(words)


        wpm = (word_count / elapsed_time) * 60 if elapsed_time > 0 else 0
        accuracy = calculate_accuracy(sentence, typed)

        # wpm = (word_count / elapsed_time) * 60 if elapsed_time > 0 else 0
        # accuracy = calculate_accuracy(sentence, typed)

        st.success("✅ Results:")
        st.write(f"- Time Taken: {round(elapsed_time, 2)} seconds")
        st.write(f"- Words Typed: {word_count}")
        st.write(f"- Typing Speed: {round(wpm, 2)} WPM")
        st.write(f"- Accuracy: {round(accuracy, 2)}%")

        return round(wpm, 2), accuracy, typed
    return None, None, None

# ----------------------------------------------------------------------------------------------------------------------
# Main app
def main():
    st.title("⌨️ Typing Speed Game")

    username = st.text_input("Enter your name:")
    difficulty = st.radio("Select Difficulty Level:", ["easy", "medium", "hard"])

    if st.button("Start Test"):
        st.session_state.sentence = random.choice(SENTENCES[difficulty])
        st.session_state.score = None

    if "sentence" in st.session_state:
        score, accuracy, typed = typing_test(st.session_state.sentence)
        if score is not None:
            save_score(username or "Anonymous", difficulty, score, accuracy)
            show_high_scores()

if __name__ == "__main__":
    main()
