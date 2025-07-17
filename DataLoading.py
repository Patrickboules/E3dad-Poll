import streamlit as st
from streamlit.components.v1 import html
import json
from github import Github
import re

def initialize_session_state():
    if 'form' not in st.session_state:
        st.session_state.form = {
            'phone_verified': False,
            'phone_number': '',
            'selected_option': None,
            'custom_topic': '',
            'is_custom_selected': False,
            'first_name': '',
            'last_name': '',
            'submitted': False,
            'temp_counts': {},
            'user_selections': {}
        }

REPO_NAME = "Patrickboules/E3dad-Poll"
FILE_PATH = "responses.json"

# Define all 22 options
options = {
    1:  ("مسئول توزيع الفرق والغرف (Logistics)", 5,"ميس إيرين"),
    2:  ("مسئول بريد السما (Multimedia)", 3,"مستر مايكل"),
    3:  ("المسئول المالي ز المشتريات", 2,"ميس نشوى"),
    5:  ("الترانيم والعزف", 5,"ميس ماريا + ميس عبير"),
    6:  ("مسئول الألعاب (Games)", 6,"ميس رشا "),
    7:  ("مسئول البرنامج", 3,"مستر مينا"),
    8:  ("الميقاتي اليومي", 5,"مستر مينا"),
    9:  ("مسئول نظام التقييم (Scoring System)", 5, "مستر مينا + ميس رشا"),
    10: ("مجموعة خلوات",2,"ميس ايرين + ميس عبير"),
    11: ("مجموعة حفلة سمر",2,"ميس رشا"),
    12: ("ترتيب القداس والحمل",1,"ميس عبير"),
}
# Validate Egyptian phone number
def validate_egyptian_phone(phone):
    # Remove any non-digit characters
    phone = re.sub(r'\D', '', phone)
    # Check if it's a valid Egyptian mobile number (starts with 01 and has 11 digits)
    if len(phone) == 11 and phone.startswith('01'):
        return phone
    return None

# Load existing responses from GitHub
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

# Calculate topic counts and user selections
def process_responses(existing_data):
    topic_counts = {num: 0 for num in options.keys()}
    user_selections = {}
    
    if isinstance(existing_data, list):
        for entry in existing_data:
            phone = entry.get("Phone", "")
            if phone:
                if phone not in user_selections:
                    user_selections[phone] = []
                
                topic = entry.get("Topic", "")
                for num, (text, _) in options.items():  # Note the unpacking here
                    if text == topic:
                        topic_counts[num] += 1
                        user_selections[phone].append(num)
                        break
    # Similarly update the dictionary case 
    # Handle case where existing_data is a dictionary (new format)
    elif isinstance(existing_data, dict):
        for phone, selection_data in existing_data.items():
            if phone not in user_selections:
                user_selections[phone] = []
            
            # Count topic selections
            topic = selection_data.get("Topic", "")
            for num, (text,_,_) in options.items():
                if text == topic:
                    topic_counts[num] += 1
                    user_selections[phone].append(num)
                    break
    
    return topic_counts, user_selections

# Save response to GitHub
def save_response():
    selected_option = st.session_state.form['selected_option']
    if selected_option:
        topic_text = options[selected_option][0]  # Get the text part
    else:
        topic_text = st.session_state.form['custom_topic']
    
    response_data = {
        "First Name": st.session_state.form['first_name'],
        "Last Name": st.session_state.form['last_name'],
        "Topic": topic_text
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
                        "Last Name": entry.get("Last Name", ""),
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


