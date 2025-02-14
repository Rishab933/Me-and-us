import streamlit as st
from PIL import Image

# Initialize session state variables
if "image_path" not in st.session_state:
    st.session_state.image_path = "US/u1.jpg"
if "caption" not in st.session_state:
    st.session_state.caption = "I have a surprise for you!!"
if "show_buttons" not in st.session_state:
    st.session_state.show_buttons = False  # Hide Yes/No initially
if "show_next" not in st.session_state:
    st.session_state.show_next = True  # Show Next button initially
if "show_next_yes" not in st.session_state:
    st.session_state.show_next_yes = False  # Show next button after Yes
if "show_next_no" not in st.session_state:
    st.session_state.show_next_no = False  # Show next button after No
if "show_video" not in st.session_state:
    st.session_state.show_video = False  # Show video only when needed
if "show_final_next" not in st.session_state:
    st.session_state.show_final_next = False  # Final Next after "No" choice
if "allow_download" not in st.session_state:
    st.session_state.allow_download = False  # Initially, no download allowed
if "download_complete" not in st.session_state:
    st.session_state.download_complete = False  # Track if download is completed


# Centered Title
st.markdown("<h1 style='text-align: center;'>HI GUNGUN !!</h1>", unsafe_allow_html=True)

# Show image only if video is not displayed
if not st.session_state.show_video:
    if st.session_state.image_path:  # Check if image exists
        image = Image.open(st.session_state.image_path)

        # Resize image dynamically based on state
        if st.session_state.image_path == "US/dont.jpg":
            image = image.resize((1000, 1400))  # Smaller image for "No" response
        elif st.session_state.image_path == "US/u2.jpg":
            image = image.resize((500,1000))
        else:
            image = image.resize((500, 500))  # Default size

        # Create Columns for Center Alignment
        col1, col2, col3 = st.columns([1, 2, 1])  # Middle column is wider

        # Display Image and Caption
        with col2:
            st.image(image, use_container_width=False)
            st.markdown(f"<h3 style='text-align: center;'>{st.session_state.caption}</h3>", unsafe_allow_html=True)

# Function to update session state when clicking "Next"
def update():
    st.session_state.image_path = "US/Me1.jpg"
    st.session_state.caption = "Do you know this guy??"
    st.session_state.show_buttons = True  # Show Yes/No buttons
    st.session_state.show_next = False  # Hide "Next" button
    st.rerun()  # Refresh UI

# Show "Next" button initially, hide after clicking
if st.session_state.show_next:
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col3:
        if st.button("Next"):
            update()  # Call function to update session state

# Show Yes/No buttons only after clicking "Next"
if st.session_state.show_buttons:
    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5, col_btn6 = st.columns([1, 1, 1, 1, 1, 1])

    def update_content():
        st.session_state.image_path = "US/Me2.jpg"  # Change to new image
        st.session_state.caption = "Oo nice 🎉🎉"
        st.session_state.show_buttons = False  # Hide Yes/No buttons
        st.session_state.show_next_yes = True  # Ensure Next button appears
        st.rerun()  # Force rerun to update UI

    def update_content_no():
        st.session_state.image_path = "US/dont.jpg"  # Change to new image
        st.session_state.caption = "Don't lie ok 😒😒"
        st.session_state.show_buttons = False  # Hide Yes/No buttons
        st.session_state.show_next_no = True  # Ensure Next button appears
        st.rerun()  # Refresh UI to show the resized image

    with col_btn3:
        if st.button("Yes"):
            update_content()  # Update state and refresh UI

    with col_btn4:
        if st.button("No"):
            update_content_no()  # Update state and refresh UI

# If "No" was selected, show a Next button to move forward
if st.session_state.show_next_no:
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col3:
        if st.button("Next", key="next_no"):
            st.session_state.caption = "You want the surprise or not 😒😒"
            st.session_state.image_path = ""  # Hide image
            st.session_state.show_next_no = False  # Hide this button
            st.session_state.show_final_next = True  # Show final Next button
            st.rerun()

# Show caption before final "Next"
if st.session_state.show_final_next and not st.session_state.show_video:
    st.markdown(f"<h3 style='text-align: center;'>{st.session_state.caption}</h3>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col3:
        if st.button("Next", key="final_next"):
            st.session_state.show_video = True  # Show video
            st.session_state.show_final_next = False  # Hide this button
            st.session_state.caption = ""  # Remove caption
            st.rerun()  # Refresh UI to display video

# Show "Next" button after Yes/No response, hide it when video appears
if st.session_state.show_next_yes and not st.session_state.show_video:
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col3:
        if st.button("Next", key="next_yes"):
            st.session_state.show_video = True  # Set flag to show video
            st.session_state.show_next_yes = False  # Hide this button after clicking
            st.session_state.image_path = ""  # Remove image
            st.session_state.caption = ""  # Remove caption
            st.rerun()  # Refresh UI to display video

# Show video only when the flag is True
if st.session_state.show_video:
    video_file = open("US/us.mp4", "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)

    # Add a question below the video
    st.markdown("### Answer this question to unlock the download:")
    correct_answer = "boobies"  # Set the correct answer
    user_answer = st.text_input("What's my happy place 😏😏", "")

    if user_answer.lower() == correct_answer:
        st.success("Correct! You can now download the video 🎉🎉")
        st.session_state.allow_download = True
    elif user_answer:
        st.error("Oops! That's not the right answer. Try again.")

    # Show download button if the answer is correct
    if st.session_state.allow_download:
        if st.download_button(
                label="Download Video 🎥",
                data=video_bytes,
                file_name="surprise_video.mp4",
                mime="video/mp4"
        ):
            st.session_state.allow_download = False  # Disable button after clicking
            st.session_state.show_video = False  # Hide the video
            st.session_state.image_path = "US/u2.jpg"
            st.session_state.caption = "Tata"
            st.rerun()  # Refresh UI to show goodbye message



