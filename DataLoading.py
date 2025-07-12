import streamlit as st
from streamlit.components.v1 import html
import json
from github import Github

REPO_NAME = "Patrickboules/E3dad-Poll"
FILE_PATH = "responses.json"

def initialize_session_state():
    if 'form' not in st.session_state:
        st.session_state.form = {
            'phone_verified': False,
            'phone_number': '',
            'selected_option': None,
            'custom_topic': '',
            'is_custom_selected': False,
            'first_name': '',
            'submitted': False,
            'temp_counts': {},
            'user_selections': {}
        }
initialize_session_state()

options = {
    1: ("مسئول توزيع الفرق والغرف (Logistics)", 5),
    2: ("مسئول بريد السما (Multimedia)", 3),
    3: ("المسئول المالي", 2),
    4: ("مسئول المشتريات", 2),
    5: ("الترانيم والعزف", 2),
    6: ("مسئول الألعاب (Games)", 6),
    7: ("مسئول البرنامج", 3),
    8: ("الميقاتي اليومي", 1),
    9: ("مسئول نظام التقييم (Scoring System)", 5)
}

@st.cache_data(ttl=1)
def load_responses():
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents(FILE_PATH)
        existing_data = json.loads(file.decoded_content.decode())
        # Ensure we return a dictionary even if the file is empty
        return existing_data if isinstance(existing_data, dict) else {}
    except Exception as e:
        st.error(f"حدث خطأ في تحميل البيانات من GitHub: {str(e)}")
        return {}
    
# Save response to GitHub
def save_response():
    response_data = {
        "First Name": st.session_state.form['first_name'],
        "Topic": options[st.session_state.form['selected_option']] if st.session_state.form['selected_option'] else st.session_state.form['custom_topic']
    }
    
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents(FILE_PATH)
        
        existing_data = json.loads(file.decoded_content.decode())
        
        # Convert list to dictionary if needed
        if isinstance(existing_data, list):
            new_data = {}
            for entry in existing_data:
                phone = entry.get("Phone", "")
                if phone:
                    new_data[phone] = {
                        "First Name": entry.get("First Name", ""),
                        "Topic": entry.get("Topic", "")
                    }
            existing_data = new_data
        
        # Update or create phone entry
        existing_data[st.session_state.form['phone_number']] = response_data
        
        repo.update_file(
            path=FILE_PATH,
            message=f"إضافة اختيار جديد من {st.session_state.form['phone_number']}",
            content=json.dumps(existing_data, indent=4, ensure_ascii=False),
            sha=file.sha
        )
        
        st.session_state.form['temp_counts'] = {}
        return True
    except Exception as e:
        st.error(f"حدث خطأ في حفظ البيانات على GitHub: {str(e)}")
        return False

def process_responses(existing_data):
    topic_counts = {num: 0 for num in options.keys()}
    user_selections = {}
    
    # Handle case where existing_data is a list (old format)
    if isinstance(existing_data, list):
        for entry in existing_data:
            phone = entry.get("Phone", "")
            if phone:
                if phone not in user_selections:
                    user_selections[phone] = []
                
                # Count topic selections
                topic = entry.get("Topic", "")
                for num, text in options.items():
                    if text == topic:
                        topic_counts[num] += 1
                        user_selections[phone].append(num)
                        break
    # Handle case where existing_data is a dictionary (new format)
    elif isinstance(existing_data, dict):
        for phone, selection_data in existing_data.items():
            if phone not in user_selections:
                user_selections[phone] = []
            
            # Count topic selections
            topic = selection_data.get("Topic", "")
            for num, text in options.items():
                if text == topic:
                    topic_counts[num] += 1
                    user_selections[phone].append(num)
                    break
    
    return topic_counts, user_selections

def get_combined_counts():
    existing_data = load_responses()
    topic_counts, _ = process_responses(existing_data)
    
    # Combine with temporary selections
    combined = topic_counts.copy()
    for num, count in st.session_state.form['temp_counts'].items():
        combined[num] += count
    return combined