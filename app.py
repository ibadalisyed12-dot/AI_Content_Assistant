import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✨",
    layout="centered"
)

# App Header
st.title("✨ AI Content Assistant")
st.markdown("Generate engaging social media captions, tailored copy, and targeted hashtags instantly using **Groq**.")

# Sidebar Configuration for API Key and Model
with st.sidebar:
    st.header("🔑 Configuration")
    api_key_input = st.text_input(
        "Enter Groq API Key",
        type="password",
        help="Get your free key from https://console.groq.com/keys"
    )
    
    st.markdown("---")
    st.markdown("### 🤖 Model Selection")
    # Popular free production model on Groq
    model_choice = st.selectbox(
    "Choose Groq Model",
    ["llama-3.1-8b-instant", "openai/gpt-oss-20b"],
    index=0
)
    
    st.markdown("---")
    st.markdown("### About")
    st.info("This tool uses Groq's high-speed inference engine to generate customized content drafts for multiple platforms.")

# Main Form for Content Inputs
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        content_type = st.selectbox(
            "Content Type",
            ["Promotional Post", "Educational / Tips", "Behind-the-Scenes", "Engagement / Question", "Announcement", "Storytelling"]
        )
        
        platform = st.selectbox(
            "Platform",
            ["LinkedIn", "X (Twitter)", "Instagram", "Facebook", "TikTok"]
        )

    with col2:
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Tech Founders, Fitness Beginners, Gen Z"
        )
        
        tone = st.selectbox(
            "Tone of Voice",
            ["Professional & Authoritative", "Casual & Friendly", "Humorous & Witty", "Inspirational & Motivational", "Direct & Bold"]
        )

    topic = st.text_area(
        "Topic / Core Message",
        placeholder="Briefly describe what you want to share or announce..."
    )
    
    submit_button = st.form_submit_button("🚀 Generate Content", use_container_width=True)

# Action on Submit
if submit_button:
    # Validate API key
    if not api_key_input:
        st.error("⚠️ Please enter your Groq API Key in the sidebar to proceed.")
    elif not topic.strip():
        st.warning("⚠️ Please provide a topic or core message for the post.")
    else:
        try:
            # Initialize Groq Client
            client = Groq(api_key=api_key_input)
            
            # Construct a detailed prompt for the LLM
            system_prompt = (
                "You are an expert social media manager and senior copywriter. "
                "Your job is to write compelling, platform-optimized posts complete with engaging hooks, "
                "clear body text, call-to-actions (CTAs), and relevant hashtags."
            )
            
            user_prompt = f"""
            Please generate a complete social media post based on the following parameters:
            - Content Type: {content_type}
            - Platform: {platform}
            - Target Audience: {target_audience if target_audience else 'General Audience'}
            - Tone: {tone}
            - Topic/Core Message: {topic}

            Format your output clearly with:
            1. **Headline / Hook**
            2. **Main Caption / Body**
            3. **Call to Action (CTA)**
            4. **Relevant Hashtags** (tailored specifically for {platform})
            """

            with st.spinner("✨ Crafting your content at lightning speed..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model=model_choice,
                    temperature=0.7,
                )
                
                generated_content = chat_completion.choices[0].message.content

            # Display Results
            st.success("🎉 Content generated successfully!")
            st.markdown("### 📝 Your Generated Post")
            st.markdown(generated_content)
            
            # Copy-friendly text box option
            with st.expander("📋 View Raw Text for Copying"):
                st.code(generated_content, language="markdown")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")