<template>
    <div class="rpg-game">
      <h1>Text-based RPG</h1>
      <p v-html="output"></p>
      <input v-model="userInput" @keyup.enter="sendInput" placeholder="Type your action here..." />
      <button @click="sendInput">Do!</button>
    </div>
  </template>
  
  <script>

  import axios from 'axios';
  
  export default {
    data() {
      return {
        userInput: '',
        output: 'You are standing in an open field west of a white house, with a boarded front door.',
      };
    },
    methods: {
      async sendInput() {
        if (this.userInput.trim()) {
          try {
            // Display user input in output
            this.output += `<br><b>You:</b> ${this.userInput}`;
            // Send input to the backend
            const response = await axios.post("http://127.0.0.1:5000/generate", { input: this.userInput });
            this.output += `<br><b>Game:</b> ${response.data.response}`;
          } catch (error) {
            console.error("Error generating response:", error);
          }
          this.userInput = ''; // Clear input field
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .rpg-game {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 8px;
  }
  input {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
  }
  button {
    padding: 10px;
    margin-top: 10px;
  }
  </style>
  