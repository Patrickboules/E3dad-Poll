from DataLoading import *
from WidgetMaker import *
import re
import time

# Configure page - disable dark mode
st.set_page_config(
    layout="wide",
    page_title="مشاريع اعداد 2025",
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

# Force light mode
st.markdown("""
<style>
    :root {
        --primary-color: #FF5722;
        --hover-color: #FFF3E0;
        --selected-color: #FFE0B2;
        --border-color: #E64A19;
        --disabled-color: #F5F5F5;
        --text-color: #333333;
        --count-color: #666666;
        --success-bg: #E8F5E9;
        --success-border: #2E7D32;
        --error-bg: #FFEBEE;
        --error-border: #F44336;
        --header-color: #FF9800;
        --custom-topic-bg: #E3F2FD;
        --custom-topic-selected: #BBDEFB;
    }
    
    html, body, [class*="css"] {
        color: var(--text-color) !important;
        background-color: white !important;
    }
    
    * {
        color: var(--text-color) !important;
    }
    
    .stApp {
        background-color: white !important;
    }
    
    .option-container {
        display: flex;
        flex-direction: column;
        margin: 8px 0;
        padding: 12px 15px;
        border-radius: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #E0E0E0;
        width: 100%;
    }
    
    .option-container:hover {
        background-color: var(--hover-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(255, 152, 0, 0.1);
    }
    
    .option-container.selected {
        background-color: var(--selected-color);
        border-left: 5px solid var(--border-color);
        box-shadow: 0 4px 8px rgba(255, 87, 34, 0.2);
    }
    
    .option-container.disabled {
        opacity: 0.7;
        pointer-events: none;
        background-color: var(--disabled-color);
    }
    
    .option-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        margin-bottom: 8px;
    }
    
    .option-text {
        text-align: right;
        font-size: 16px;
        color: var(--text-color);
        width: 100%;
        padding: 5px 0;
    }
    
    .progress-container {
        width: 100%;
        height: 20px;
        background-color: #F5F5F5;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-color), #FF8A65);
        width: 0%;
        transition: width 0.5s ease;
    }
    
    .complete {
        background: linear-gradient(90deg, var(--border-color), var(--primary-color));
    }
    
    .option-number {
        font-weight: bold;
        font-size: 16px;
        color: var(--text-color);
    }
    
    .count-display {
        font-size: 13px;
        color: var(--count-color);
        font-weight: 500;
    }
    
    .required-field::after {
        content: " *";
        color: red;
        position: absolute;
        margin-left: 2px;
    }
    
    .stButton>button {
        border-radius: 8px;
        padding: 8px 16px;
        transition: all 0.3s;
        width: 100%;
        background-color: var(--primary-color);
        color: white !important;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(255, 87, 34, 0.3);
    }
    
    .stButton>button:disabled {
        background-color: #cccccc !important;
        cursor: not-allowed;
    }
    
    .header {
        color: var(--header-color);
        margin-bottom: 20px;
    }
    
    .success-message {
        background-color: var(--success-bg);
        border-left: 5px solid var(--success-border);
        font-size: 18px;
        padding: 15px;
        border-radius: 8px;
        color: #333333;
        margin: 20px 0;
    }
    
    .error-message {
        background-color: var(--error-bg);
        border-left: 5px solid var(--error-border);
        font-size: 16px;
        padding: 10px;
        border-radius: 6px;
        color: #333333;
        margin: 10px 0;
    }
    
    .custom-topic-container {
        background-color: var(--custom-topic-bg);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #BBDEFB;
        transition: all 0.3s ease;
    }
    
    .custom-topic-selected {
        background-color: var(--custom-topic-selected);
        border-left: 5px solid var(--border-color);
    }
    
    .custom-topic-input {
        display: flex;
        gap: 10px;
        align-items: center;
    }
    
    .custom-topic-input input {
        flex-grow: 1;
    }
    
    .custom-topic-input button {
        flex-shrink: 0;
        width: 100px !important;
        height: 38px;
        margin-top: 10px;
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        color: #333333 !important;
        background-color: white !important;
        border: 1px solid #E0E0E0 !important;
    }
    
    /* Phone verification container */
    .phone-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background-color: white;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .option-text {
            font-size: 14px;
        }
        
        .option-number, .count-display {
            font-size: 14px;
        }
        
        .progress-container {
            height: 15px;
        }
        
        .stButton>button {
            padding: 10px;
            font-size: 14px;
        }
        
        .stTextInput>div>div>input {
            font-size: 14px;
        }
        
        .custom-topic-input {
            flex-direction: column;
        }
        
        .custom-topic-input button {
            width: 100% !important;
        }
        
        .phone-container {
            padding: 20px;
        }
    }
    
    /* Disable dark mode */
    [data-testid="stAppViewContainer"] {
        background-color: white !important;
    }
    
    [data-testid="stHeader"] {
        background-color: white !important;
    }
    
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    [data-testid="stDecoration"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 مشاريع اعداد 2025")

initialize_session_state()

# Validate Egyptian phone number
def validate_egyptian_phone(phone):
    # Remove any non-digit characters
    phone = re.sub(r'\D', '', phone)
    # Check if it's a valid Egyptian mobile number (starts with 01 and has 11 digits)
    if len(phone) == 11 and phone.startswith('01'):
        return phone
    return None

def option_click_js():
    return """
    <script>
    function handleClick(optionNum) {
        const buttons = parent.document.querySelectorAll('button[title="اختر"]');
        buttons.forEach(button => {
            if (button.textContent.includes("اختر") && 
                button.getAttribute("data-testid").includes(optionNum)) {
                button.click();
            }
        });
    }

    function enforceLightMode() {
        document.documentElement.style.backgroundColor = '#ffffff';
        document.documentElement.style.colorScheme = 'light';
        document.body.style.backgroundColor = '#ffffff';
        document.body.classList.remove('dark');

        const darkModeToggle = document.querySelector('[data-testid="stToolbar"]');
        if (darkModeToggle) darkModeToggle.style.display = 'none';
    }

    // Initial call and interval check
    window.addEventListener('load', enforceLightMode);
    setInterval(enforceLightMode, 500);
    </script>
    """

def phone_verification_page():
    with st.container():
        # Custom CSS for better styling
        st.markdown("""
        <style>
            .phone-verification-container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                background-color: #ffffff;
            }
            .phone-header {
                text-align: center;
                color: #2c3e50;
                margin-bottom: 25px;
            }
            .phone-instructions {
                text-align: center;
                color: #7f8c8d;
                margin-bottom: 30px;
                font-size: 16px;
                line-height: 1.5;
            }
            .stTextInput input {
                text-align: right;
                direction: rtl;
                padding: 12px;
                font-size: 16px;
                width: 100%;
            }
            .phone-actions {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }
            .existing-data-card {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
                margin: 20px 0;
                border-left: 4px solid #3498db;
            }
            .data-item {
                margin-bottom: 8px;
                display: flex;
            }
            .data-label {
                font-weight: bold;
                min-width: 120px;
                color: #2c3e50;
            }
            .data-value {
                flex-grow: 1;
                color: #34495e;
            }
            /* Make button same width as text input */
            .stButton>button {
                width: 100%;
                padding: 12px;
                font-size: 16px;
            }
        </style>
        """, unsafe_allow_html=True)

        # Main container
        st.markdown("""
        <div class="phone-verification-container">
            <div class="phone-header">
                <h2>التحقق من رقم هاتفك انه متسجل لدينا</h2>
            </div>
            <div class="phone-instructions">
                <p>الرجاء إدخال رقم الهاتف المصري (يبدأ بـ 01 ويحتوي على 11 رقمًا)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Phone number input
        phone = st.text_input(
            "",
            key="phone_input",
            placeholder="أدخل رقم هاتفك (مثال: 01234567890)",
            max_chars=11,
            label_visibility="collapsed"
        )
        
        # Verification button
        if st.button("Enter", 
                    use_container_width=True,
                    type="primary"):
            validated_phone = validate_egyptian_phone(phone)
            if validated_phone:
                # Load existing data
                existing_data = load_responses()
                
                # Check if phone exists in data
                if validated_phone in existing_data:
                    user_data = existing_data[validated_phone]
                    st.session_state.form.update({
                        'phone_number': validated_phone,
                        'first_name': user_data.get('First Name', ''),
                        'last_name': user_data.get('Last Name', ''),
                        'selected_option': next((num for num, text in options.items() if text == user_data.get('Topic', '')), None),
                        'custom_topic': '' if any(user_data.get('Topic', '') == text for text in options.values()) else user_data.get('Topic', ''),
                        'is_custom_selected': not any(user_data.get('Topic', '') == text for text in options.values()),
                        'phone_verified': True
                    })
                    
                    # Show existing data in a nice card
                    st.markdown("""
                    <div class="existing-data-card">
                        <h4 style="margin-top: 0; color: #2c3e50;">البيانات المسجلة سابقاً</h4>
                        <div class="data-item">
                            <div class="data-label">الاسم الأول:</div>
                            <div class="data-value">{}</div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">الاسم الأخير:</div>
                            <div class="data-value">{}</div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">الموضوع المختار:</div>
                            <div class="data-value">{}</div>
                        </div>
                    </div>
                    """.format(
                        user_data.get('First Name', ''),
                        user_data.get('Last Name', ''),
                        user_data.get('Topic', '')
                    ), unsafe_allow_html=True)
                    
                    # Only show the "Continue with existing data" button
                    if st.button("المتابعة بالبيانات المسجلة", 
                            use_container_width=True,
                            type="primary"):
                        st.session_state.form['phone_verified'] = True
                        st.markdown.clear()
                        st.rerun()
                    
                else:
                    # New phone number - automatically redirect
                    st.session_state.form.update({
                        'phone_number': validated_phone,
                        'first_name': '',
                        'second_name': '',
                        'selected_option': None,
                        'custom_topic': '',
                        'is_custom_selected': False,
                        'phone_verified': True
                    })
                    
                    # Check if user has reached max selections
                    _, user_selections = process_responses(existing_data)
                    user_topics = user_selections.get(validated_phone, [])
                    
                    if len(user_topics) >= 3:
                        st.error("""
                        <div style='text-align: center; padding: 15px; border-radius: 8px; background-color: #fdecea;'>
                            لقد قمت بالفعل باختيار 3 مواضيع كحد أقصى لكل رقم هاتف.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.rerun()  # Automatically redirect to choices page
                        
            else:
                st.error("""
                <div style='text-align: center; padding: 15px; border-radius: 8px; background-color: #fdecea;'>
                    الرجاء إدخال رقم هاتف مصري صحيح (يبدأ بـ 01 ويحتوي على 11 رقمًا)
                </div>
                """, unsafe_allow_html=True)

def main_form():
    if st.session_state.form['submitted'] == True:
            show_confirmation_page()
            return
    else:
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = time.time()
        
        # Check if it's time to refresh data (every 30 seconds)
        current_time = time.time()
        if current_time - st.session_state.last_refresh > 5:
            st.session_state.last_refresh = current_time
            st.rerun()
        with st.container():
            st.markdown("""
<div style="text-align: center; font-size: 20px;">

### كيفية استخدام النموذج:

1 .إذا كنت بمفردك، يرجى ملء حقل الاسم الأول فقط.  
2 .إذا كان لديك زميل في الفريق، يرجى ملء اسمه أيضًا.  
3 .كل اختيار تقوم به سيتم حفظه تلقائيًا.  
4 .يجب عليك الضغط على زر "اختيار" لتأكيد اختيارك، حتى في حالة الإجابة الحرة.  
5 .لا بد من تقديم النموذج بالضغط على زر "إرسال" لتأكيد اختياراتك.  

**ملاحظة:** التأكد من اتباع جميع الخطوات لضمان تسجيل إجاباتك بشكل صحيح.

</div>
""", unsafe_allow_html=True)
            
            st.markdown('<span class="required-field">اسم المخدوم رقم 1</span>', unsafe_allow_html=True)
            st.session_state.form['first_name'] = st.text_input(
                            "اسم المخدوم رقم 1", 
                            value=st.session_state.form['first_name'],
                            key="first_name_input",
                            label_visibility="collapsed",
                        )
            
            st.markdown("---")
            
            existing_data = load_responses()  # @st.cache_data(ttl=1) ensures freshness
            _, user_selections = process_responses(existing_data)
                    
                    # Display topic selection options
            st.markdown('<h2 class="header">الرجاء اختيار موضوع واحد من المواضيع التالية:</h2>', unsafe_allow_html=True)
                    
            for num, (text,limit) in options.items():
                create_option(num, text, user_selections,limit)
                    
            html(option_click_js(), height=0)
            st.markdown("---")

            ##create_custom_topic_input() can be used if needed 

            has_valid_selection = st.session_state.form['selected_option'] is not None
                      
            is_first_name_empty = not st.session_state.form.get('first_name', '').strip()

                    # Determine if the submit button should be disabled
            submit_disabled = not has_valid_selection or is_first_name_empty

                    # Display error messages
            if not has_valid_selection:
                    st.markdown(
                            '<div class="error-message">'
                            'الرجاء اختيار موضوع واحد أو كتابة موضوع مخصص'
                            '</div>',
                            unsafe_allow_html=True
                        )

            if is_first_name_empty and has_valid_selection:
                    st.markdown(
                            '<div class="error-message">'
                            'الرجاء إدخال اسم المخدوم رقم 1'
                            '</div>',
                            unsafe_allow_html=True
                        )

                    # Submit button
            if submit_disabled:
                st.button("✅ إرسال الاختيار",
                                type="primary",
                                key="submit_btn",
                                use_container_width=True,
                                disabled=True)
            else:
                if st.button("✅ إرسال الاختيار",
                                    type="primary",
                                    key="submit_btn",
                                    use_container_width=True):
                    if save_response():
                            st.session_state.form['submitted'] = True
                            st.rerun()


def show_confirmation_page():
    st.empty()
    st.balloons()
    # Get the selected topic
    topic = (options[st.session_state.form['selected_option']] 
            if st.session_state.form['selected_option'] 
            else st.session_state.form['custom_topic'])

    st.markdown(
            f"""
            <div style="
                padding: 1.5rem;
                background: white;
                border-radius: 10px;
                margin: 1rem 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            ">
                <h3 style='color: #1976d2; text-align: center;'>تفاصيل التسجيل</h3>
                <div style="text-align: right;">
                    <p><strong>الاسم:</strong> {st.session_state.form['first_name']}</p>
                    <p><strong>الموضوع المختار:</strong> {topic}</p>
                    <p><strong>رقم الهاتف:</strong> {st.session_state.form['phone_number']}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

def main():
    if not st.session_state.form['phone_verified']:
        phone_verification_page()
    else:
        main_form()

    time.sleep(5)
    st.rerun()

if __name__ == "__main__":
    main()