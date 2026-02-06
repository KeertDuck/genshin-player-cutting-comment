import streamlit as st
import calculate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

def get_api_key(key_name):
    try:
        # 优先尝试从Secrets中获取
        return st.secrets.get(key_name)
    except (KeyError, FileNotFoundError):
        # 如果在Secrets中没找到，则回退到本地环境变量（用于开发）
        load_dotenv()
        return os.environ.get(key_name)

llm = ChatOpenAI(
    model="moonshot-v1-8k",  # 可换成 32k 或 128k
    temperature=0.9,
    max_tokens=800,
    openai_api_key=get_api_key("KIMI_API_KEY"),
    openai_api_base="https://api.moonshot.cn/v1",
)

# 页面配置
st.set_page_config(page_title="原神玩家锐评工具", page_icon="💀", layout="centered")

# 初始化 session_state
if "massage" not in st.session_state:
    st.session_state.massage = {
        "age": None,
        "gender": None,
        "height": "",
        "weight": "",
        "best_character": ""
    }
# 初始化 session_state 中的页面状态
if "page" not in st.session_state:
    st.session_state.page = "form"  # 两个状态: “form” 或 “result”
#原神角色图
character_image_map = {
    "雷电将军": "https://wiki.biligame.com/ys/特殊:重定向/file/无背景-角色-雷电将军.png",
    "神里绫华": "https://wiki.biligame.com/ys/特殊:重定向/file/无背景-角色-神里绫华.png",
    "胡桃": "https://wiki.biligame.com/ys/特殊:重定向/file/无背景-角色-胡桃.png",
    "纳西妲": "https://wiki.biligame.com/ys/特殊:重定向/file/无背景-角色-纳西妲.png",
    "芙宁娜": "https://wiki.biligame.com/ys/特殊:重定向/file/无背景-角色-芙宁娜.png",
    # 更多角色可以按照此格式自行添加
    # 格式为：https://wiki.biligame.com/ys/特殊:重定向/file/无背景-角色-{角色名}.png
    # 角色名需要是中文，且与WIKI内文件名完全一致。
}

#第一部分
@st.fragment()
def part_1():
    st.title("💀💀💀原神玩家锐评工具")
    st.caption("什么，你是原神玩家？输入下面的信息来找骂😋")

@st.fragment()
def part_2():
    if st.session_state.page == "form":
        with st.form(key="my_form"):
            # 将输入直接保存到 session_state
            st.session_state.massage["age"]=st.slider(label="年龄:",min_value=0,max_value=100)
            st.session_state.massage["gender"]=st.radio(label="性别:",options=["男","女"])
            st.session_state.massage["height"]=st.text_input(label="身高(cm):")
            st.session_state.massage["weight"]=st.text_input(label="体重(kg):")
            st.session_state.massage["best_character"]=st.text_input(label="最喜欢的原神角色")

            form_submitted = st.form_submit_button(label="确认！")

            if form_submitted:

                if (st.session_state.massage["age"] is not None and
                    st.session_state.massage["gender"] is not None and
                    st.session_state.massage["height"].strip() != "" and
                    st.session_state.massage["weight"].strip() != "" and
                    st.session_state.massage["best_character"].strip() != ""):
                    st.warning("✅ 信息已提交！😋开始想办法攻击你...🤩")
                    st.session_state.page = "result"
                    st.rerun()
                else:
                    st.spinner("请输入全部的信息！😡")
    elif st.session_state.page == "result":
        # 模拟一个有趣的生成过程（带进度条）
        # progress_bar = st.progress(0)
        # status_text = st.empty()
        # for percent in range(101):
        #     time.sleep(0.01)  # 模拟耗时
        #     progress_bar.progress(percent)
        #     status_text.text(f"正在思考你的心理薄弱点... 🧐{percent}%")
        with st.spinner("正在思考你的心理薄弱点... 🧐"):
            st.divider()

            try:
                height = float(st.session_state.massage["height"])  # 或 int(height_str)，但身高可能有小数
                weight = float(st.session_state.massage["weight"])
            except ValueError:
                st.error("❌ 请输入有效的数字（可带小数点，如175、175.5），不要输入字母或特殊符号！")
            result_comment = calculate.cutting_comment(st.session_state.massage["age"],
                                                       height,
                                                       weight,
                                                       st.session_state.massage["best_character"])
            comments_str = "，".join(result_comment)
            messages = [
                SystemMessage(content="""你是一个用于生成有趣的对话的机器，
                本次你将要扮演一个朋友使用尖酸刻薄的语气来对原神玩家进行评价。
                要求：
                - 语句要流畅通顺
                - 使用相当尖酸刻薄的语气进行嘲讽
                - 段落中多增加嘲讽的emoji表情包来增强情绪效果
                - 输出纯正文，不要任何说明、标题、前言后语"""),
                HumanMessage(content=f"""根据下面的句段内容生成评价：{comments_str}""")
            ]
            response = llm.invoke(
                messages,
                temperature=0.9,
                max_tokens=800
            )
            result = response.content.strip()
            st.markdown(
                f"<h3 style='text-align: center;'>{result}</h3>",
                unsafe_allow_html=True)
            # st.write(comments_str)


        # 提供一个“重新生成”按钮，返回表单页
        if st.button("😡 我不服气！，重新填写"):
            st.session_state.page = "form"
            st.rerun()



part_1()
part_2()