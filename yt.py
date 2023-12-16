import streamlit as st
from transformers import pipeline
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

# Function to get video ID from YouTube link
def get_video_id(link):
    return link.split("=")[1]

# Function to get video duration in minutes
def get_video_duration(link):
    video_id = get_video_id(link)
    try:
        ydl = yt_dlp.YoutubeDL()
        info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        duration = info_dict.get('duration', 0) // 60  # Convert to minutes
        return duration
    except Exception as e:
        st.error(f"Error retrieving video information: {e}")
        return 0

# Function to summarize the transcript
def summarize_video(link, max_lines=15):
    video_id = get_video_id(link)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    result = " ".join([i['text'] for i in transcript])

    summarizer = pipeline('summarization')
    num_iters = int(len(result) / 1000)
    summarized_text = []

    for i in range(0, num_iters + 1):
        start = i * 1000
        end = (i + 1) * 1000
        chunk = result[start:end]

        out = summarizer(chunk)
        out = out[0]['summary_text']
        summarized_text.append(out)

    # Join the summarized texts into a single paragraph
    summarized_paragraph = " ".join(summarized_text)

    # Limit the output to a certain number of lines based on video duration
    max_chars = get_video_duration(link) * 120  # Assuming an average of 120 characters per line
    summarized_paragraph = summarized_paragraph[:max_chars]

    # Split the summarized text into lines
    summarized_lines = summarized_paragraph.split("\n")[:max_lines]
    summarized_result = "\n".join(summarized_lines)

    return summarized_result

# Streamlit app
def main():
    st.title("YouTube Video Summarizer")

    # User input: YouTube link
    youtube_link = st.text_input("Enter YouTube video link:")
    
    if st.button("Summarize"):
        # Check if the link is provided
        if not youtube_link:
            st.warning("Please enter a YouTube video link.")
        else:
            # Summarize and display the result
            summarized_result = summarize_video(youtube_link)
            st.write("Summarized text:\n" + summarized_result)

if __name__ == "__main__":
    main()


    

