from tkinter import *
import customtkinter
import openai
import os
import pickle

#initiate app
root = customtkinter.CTk()
root.title("ChatGPT Bot")
root.geometry('600x600')
root.iconbitmap('ai_lt.ico')

#set color scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

#create text frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

# add text widget to get ChatGPT Responses
my_text = Text(text_frame, 
	bg="#343638", 
	width=64, 
	border=1, 
	fg="#d6d6d6",
	relief="flat",
	wrap=WORD,
	selectbackground="#1f538d"
	)
my_text.grid(row=0, column=0)

#submit to ChatGPT
def speak():
	if chat_entry.get():
		try:
			#check for API key
			filename = "api_key"
			if os.path.isfile(filename):
				input_file = open(filename, 'rb')

				key = pickle.load(input_file)

				#query ChatGPT
				openai.api_key = key

				#create instance
				openai.Model.list()

				#define query
				response = openai.Completion.create(
					model = "text-davinci-003",
					prompt = chat_entry.get(),
					temperature = 0,
					max_tokens = 60,
					top_p = 1.0,
					frequency_penalty = 0.0,
					presence_penalty = 0.0,
					)

				my_text.insert(END, chat_entry.get())
				my_text.insert(END, "\n")
				my_text.insert(END, (response["choices"][0]["text"].strip()))
				my_text.insert(END, "\n\n")
				chat_entry.delete(0, END)
			else:
				input_file = open(filename, 'wb')
				input_file.close()
				my_text.insert(END, "\n\n You need an API Key to talk with ChaGPT. \n\n")

		except Exception as e:
			my_text.insert(END, f"\n\n There was an error\n\n{e}")	
	else:
		my_text.insert(END, "\n\nYou didn't ask anything!\n\n")

#clear the screens
def clear():

	#clear main text box
	my_text.delete(1.0, END)
	chat_entry.delete(0, END)


#do api things
def key():

	try:
		#define filename
		filename = "api_key"
		if os.path.isfile(filename):
			input_file = open(filename, 'rb')

			key = pickle.load(input_file)

			api_entry.insert(END, key)
		else:
			input_file = open(filename, 'wb')
			input_file.close()
	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")


	#resize app
	root.geometry('600x750')
	#show api_frame
	api_frame.pack(pady=30)

#do api things
def save_key():
	try:
		filename = "api_key"

		output_file = open(filename, 'wb')
		pickle.dump(api_entry.get(), output_file)

		api_entry.delete(0,END)
	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")

	#show API frame
	api_frame.pack_forget()
	root.geometry('600x600')
	
	pass

#scrollbar for text widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
	command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky="ns")

#add scrollbar to textbox
my_text.configure(yscrollcommand=text_scroll.set)


#Add entry widget to ask questions

chat_entry = customtkinter.CTkEntry(root,
	placeholder_text="Talk to ChatGPT",
	width=535,
	height=50,
	border_width=1)
chat_entry.pack(pady=10)

#create button frame (so buttons will go in a row and use the grid system)
button_frame = customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

#add buttons
submit_button = customtkinter.CTkButton(button_frame,
	text="Ask",
	command=speak)
submit_button.grid(row=0, column=0, padx=25)

clear_button = customtkinter.CTkButton(button_frame,
	text="Clear Screen",
	command=clear)
clear_button.grid(row=0, column=1, padx=35)

api_button = customtkinter.CTkButton(button_frame,
	text="Update API Key",
	command=key)
api_button.grid(row=0, column=2, padx=25)


#add API key frame

api_frame = customtkinter.CTkFrame(root, border_width=1)


#add API entry input field
api_entry = customtkinter.CTkEntry(api_frame, 
	placeholder_text="Enter your API Key",
	width=350,
	height=50,
	border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)
api_save_button = customtkinter.CTkButton(api_frame,
	text="Save Key",
	command=save_key)
api_save_button.grid(row=0, column=1, padx=10)

#show/hide API Key Frame

root.mainloop()