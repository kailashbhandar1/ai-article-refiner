import streamlit as st
import openai
import os

# Get API key from Streamlit Secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

# Call OpenAI API
def refine_article(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1000
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Web App Interface
st.set_page_config(page_title="AI Article Refiner", layout="wide")
st.title("📝 AI Article Refiner")

article_input = st.text_area("📄 Paste your article draft below:", height=300)
mode = st.radio("Choose Refinement Mode", [
    "Only Refine",
    "Refine + Add Missing Points",
    "Refine + Use Provided Keywords",
    "All 3 (Refine + Add Points + Keywords)"
])

keywords_input = ""
if mode in ["Refine + Use Provided Keywords", "All 3 (Refine + Add Points + Keywords)"]:
    keywords_input = st.text_area("🔑 Paste target SEO keywords (comma-separated):", height=100)

if st.button("Refine Article"):
    if article_input.strip() == "":
        st.warning("Please paste an article to refine.")
    else:
        with st.spinner("Refining your article..."):
            if mode == "Only Refine":
                prompt = f"""
Refine the following article:
- Improve grammar, tone, and structure
- Optimize for SEO and readability
- Ensure it’s plagiarism-free and publication-ready
- Provide a meta title, meta description, and URL slug

Article:
{article_input}
"""

            elif mode == "Refine + Add Missing Points":
                prompt = f"""
Refine the following article:
- Improve grammar, tone, and structure
- Optimize for SEO and readability
- Add missing but important points typically included in this topic
- Ensure it’s plagiarism-free and publication-ready
- Provide a meta title, meta description, URL slug, and 2-3 FAQs

Article:
{article_input}
"""

            elif mode == "Refine + Use Provided Keywords":
                prompt = f"""
Refine the following article:
- Improve grammar, tone, and structure
- Optimize for SEO by naturally including the provided keywords
- Ensure it’s plagiarism-free and publication-ready
- Provide a meta title, meta description, URL slug, and 2-3 FAQs

Keywords:
{keywords_input}

Article:
{article_input}
"""

            else:  # All 3
                prompt = f"""
Refine the following article:
- Improve grammar, tone, and structure
- Optimize for SEO by naturally including the provided keywords
- Add any missing but important points related to the topic
- Ensure it’s plagiarism-free and publication-ready
- Provide a meta title, meta description, URL slug, and 2-3 FAQs

Keywords:
{keywords_input}

Article:
{article_input}
"""

            output = refine_article(prompt)
            st.markdown("### ✅ Refined Article Output")
            st.write(output)
            st.download_button("📥 Download Refined Article", data=output, file_name="refined_article.txt")
