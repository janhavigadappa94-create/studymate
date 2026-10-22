import streamlit as st
from datetime import date
import json
from pathlib import Path
#overall appearance
st.set_page_config(page_title="StudyMate",page_icon="📚",layout="wide")

#css to improve inteference of app 
# CSS to improve the appearance of StudyMate
st.markdown("""

<style>
   
/* Main sage-green app background */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stHeader"] {
    background-color: #F2F7F1 !important;
}

/* Keep the top header transparent */
[data-testid="stHeader"] {
    background-color: transparent !important;
}

    /* All headings */
    h1, h2, h3 {
        color: #355B46;
    }

    /* White metric cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #B8D5BE !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(23, 59, 50, 0.10) !important;
    }

    /* Metric numbers */
    [data-testid="stMetricValue"] {
        color: #173B32 !important;
        font-weight: 700;
    }

    /* Metric labels */
    [data-testid="stMetricLabel"] {
        color: #52715B !important;
        font-size: 14px;
    }
    

/* Rounded task cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px !important;
    border: 1px solid #D5E3D6 !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(23, 59, 50, 0.07) !important;
    padding: 12px !important;
    margin-bottom: 12px !important;
    transition: box-shadow 0.2s ease-in-out;
}


/* Welcome banner */
.welcome-header {
    background: linear-gradient(135deg, #D5E8D8, #E8F1E7) !important;
    padding: 30px 28px !important;
    border-radius: 20px !important;
    margin-bottom: 24px !important;
    display: block !important;
    border: 1px solid #C5DCC9 !important;
    box-shadow: 0 5px 16px rgba(23, 59, 50, 0.08) !important;
}

/* Welcome title */
.welcome-header h1 {
    color: #355B46 !important;
    margin: 0 0 12px 0 !important;
    font-size: 34px !important;
    font-weight: 750 !important;
}

/* Welcome subtitle */
.welcome-header p {
    color: #52715B !important;
    margin: 0 0 7px 0 !important;
    font-size: 16px !important;
    line-height: 1.6 !important;
}
 

    /* Make progress bars more visible */
    [data-testid="stProgress"] > div {
        background-color: #D5E8D8 !important;
        border-radius: 10px !important;
        overflow: hidden;
    }

    [data-testid="stProgress"] [role="progressbar"] > div {
        background-color: #43845B !important;
        border-radius: 10px !important;
    }

    /* Stronger, clearer text */
    .stApp {
        color: #263D30;
    }

    /* Give section headings a little more emphasis */
    h2, h3 {
        color: #355B46 !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px;
    }


/* Overall page spacing */
[data-testid="stMainBlockContainer"] {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
}

/* Consistent spacing between sections */
div[data-testid="stVerticalBlock"] {
    gap: 1rem;
}

/* Align metric cards neatly */
[data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
}

/* Keep headings clean and readable */
h1, h2, h3 {
    letter-spacing: -0.3px;
}

/* Better spacing around section headings */
h2 {
    margin-top: 1.5rem !important;
    margin-bottom: 1rem !important;
}

/* Comfortable spacing for buttons */
.stButton > button {
    border-radius: 10px !important;
    transition: all 0.2s ease-in-out;
}
/* Make Subject and Topic fields clearly visible */
.stTextInput input,
.stNumberInput input {
    color: #263D30 !important;
    background-color: #FFFFFF !important;
}

/* Make input labels visible */
.stTextInput label,
.stSelectbox label,
.stDateInput label,
.stNumberInput label {
    color: #263D30 !important;
}

/* Make ADD TASK button visible */
.stButton > button {
    background-color: #355B46 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    padding: 10px 20px !important;
}
/* Fix text visibility on yellow backgrounds */
.stAlert,
.stAlert p,
.stAlert div,
[data-testid="stNotificationContent"] {
    color: #263D30 !important;
}

/* Make priority and dropdown text visible */
.stSelectbox div,
.stSelectbox span,
.stSelectbox input {
    color: #263D30 !important;
}

/* Make highlighted text readable */
.stMarkdown p,
.stMarkdown span {
    color: #263D30;
}
</style>

""", unsafe_allow_html=True)

st.markdown("""
<div class="welcome-header">
    <h1>📚 StudyMate</h1>
    <p>Plan. Study. Progress.</p>
    <p>Stay organized, one task at a time.</p>
</div>
""", unsafe_allow_html=True)

TASK_FILE=TASKS_FILE = Path(__file__).parent / "tasks.json"
#dump json

def save_tasks():
    tasks_to_save = []

    for task in st.session_state.tasks:
        saved_task = task.copy()
        saved_task["deadline"] = str(saved_task["deadline"])
        tasks_to_save.append(saved_task)

    with open(TASK_FILE, "w") as file:
        json.dump(tasks_to_save, file, indent=4)
#load
if "tasks" not in st.session_state:
    if TASK_FILE.exists():
        with open(TASK_FILE, "r") as file:
            st.session_state.tasks = json.load(file)

        for task in st.session_state.tasks:
            task["deadline"] = date.fromisoformat(task["deadline"])
    else:
        st.session_state.tasks = []

st.header("➕ Add Study Task")
subject=st.text_input("Subject")
topic=st.text_input("Topic")
priority=st.selectbox("Priority",["High","Medium","Low"])
deadline=st.date_input("Deadline")
study_time=st.number_input("⌚Estimated Study Time(Minutes)",min_value=15,step=15)

if st.button("ADD TASK"):
    st.session_state.tasks.append({"subject":subject,"topic":topic,"priority":priority,"deadline":deadline,"study_time":study_time,"completed":False})
    save_tasks()
    st.success("TASK ADDED SUCCESSFULLY!✔️")
filter_option=st.selectbox("🔍Filter Tasks",["All","High","Medium","Low"])

search=st.text_input("Search Tasks",placeholder="search by Subject  or Topic")
for i,task in enumerate(st.session_state.tasks):
    task["completed"]=st.session_state.get(f"completed_{i}",task.get("completed",False))

total_tasks=len(st.session_state.tasks)

#completed count for per subject
subject_completed={}
for task in st.session_state.tasks:
     subject=task["subject"]
     if task["completed"]:
         if subject not in subject_completed:
              subject_completed[subject]=0
         subject_completed[subject]+=1

#total tasks belong to each subject
subject_total={}
for task in st.session_state.tasks:
     subject=task["subject"]
     if subject not in subject_total:
         subject_total[subject]=0
     subject_total[subject]+=1

#calculate each subject percentage
subject_progress={}
for subject in subject_total:
     total=subject_total[subject]
     completed=subject_completed.get(subject,0)
     if total>0:
        subject_progress[subject]=(completed / total*100)
     else:
         subject_progress[subject]=0

#display subject progress
st.subheader("📚 Subject Progress")
for subject,progress_value in subject_progress.items():
    st.write(f"**{subject}**-{progress_value:.1f}%")
    st.progress(progress_value/100)


#shows all completed tasks
completed_tasks=sum(1 for task in st.session_state.tasks if task["completed"])

#for pending task display
pending_tasks=total_tasks-completed_tasks

#progress in %
progress=(completed_tasks/total_tasks*100) if total_tasks>0 else 0

st.subheader("📊 Study Dashboard")
col1,col2,col3=st.columns(3)
with col1:
    st.metric(label="📚 Total Task",value=total_tasks)
with col2:
    st.metric(label="✔️Completed Tasks",value=completed_tasks,delta=f"{progress:.1f}%")
with col3:
    st.metric(label="⌛Pending Task",value=pending_tasks)

#divides with a horizantal line
st.divider()
st.subheader("📈Overall Progress")
st.progress(progress/100)
st.write(f"You have completed {progress:.1f}% of your tasks!")
if progress==100:
    st.success("🎉Amazing!All Tasks Completed")
elif progress>=50:
    st.info("👏Great progress! Keep Going!")
else:
    st.warning("💪 Keep Working!")

st.subheader("📆Exam Countdown")
exam_name=st.text_input("Enter Exam Name")
exam_date=st.date_input("Select Exam Date")
days_left=(exam_date-date.today()).days
if exam_name:
    st.info(f"📚{exam_name} exam:{days_left} days left")

st.divider()
st.subheader("⌚Study Time Overview")

total_study_time=sum(task["study_time"]
    for task in st.session_state.tasks)
study_hours=total_study_time/60
daily_target=180
study_progress=min(total_study_time/daily_target,1.0)

st.write("🎯Daily Study Target")
st.progress(study_progress)

st.write(f"{study_progress*100:.1f}% of daily target completed")

col1,col2=st.columns(2)
with col1:
    st.metric("⌚Total Minutes",total_study_time)
with col2:
    st.metric("⌚Total Hours",f"{study_hours:.1f} hours")

st.subheader("🎯Today's Study Tasks")
today=date.today()
today_tasks=[ task for task in st.session_state.tasks if task["deadline"]==today]
if today_tasks:
     for task in today_tasks:
         with st.container(border=True):
             st.write("📚 Subject:",task["subject"])
             st.write("📖 Topic:",task["topic"])
             st.write("⭐ Priority:", task["priority"])
             if task["completed"]:
                 st.write("status:completed")
             else: 
                 st.write("status:pending")
else:
     st.info("🎉 No Tasks Due Today!")

#2nd part of app
#st.header("📋MY TASKS")
st.markdown("## 📋My Tasks")
st.caption("stay organized,track your progress , and keep moving forward")

for i, task in enumerate(st.session_state.tasks):
    if filter_option!="All"and task["priority"]!=filter_option:
        continue
    if search and search.lower() not in task["subject"].lower() and search.lower() not in task["topic"].lower():
        continue
           
    with st.container(border=True):
        st.markdown(f"### 📚 {task['subject']}")
        st.write(f"📖 **Topic:** {task['topic']}")

        if task["priority"] == "High":
            st.error("🔴 Priority: High")
        elif task["priority"] == "Medium":
            st.warning("🟡 Priority: Medium")
        else:
            st.success("🟢 Priority: Low")

        st.write(f"📆 **Deadline:** {task['deadline']}")

        if not task["completed"] and task["deadline"] < date.today():
            st.error("This task is overdue!")
        elif not task["completed"] and (task["deadline"] - date.today()).days <= 2:
            st.warning("Deadline approaching!")

        st.write(f"⌚ **Study Time:** {task['study_time']} minutes")

        completed = st.checkbox(
              "Completed",
        value=task.get("completed", False),
            key=f"completed_{i}"
)
        if task.get("completed",False)!=completed:
             task["completed"] = completed
             save_tasks()

        if st.button("🗑️ Delete", key=f"delete_{i}"):
            st.session_state.tasks.pop(i)
            save_tasks()
            st.rerun()
