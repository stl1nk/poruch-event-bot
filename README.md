# 🎉 Poruch Charity Raffle Telegram Bot

A Telegram bot built for the **"Poruch" Charity Event** to run a raffle contest.

## 🤖 Features

- 💬 Users can register to participate in the charity raffle.
- 🎟️ Admin can:
  - Randomly select a winner.
  - Reset the contest and ask users to re-register.
- 🔒 Only the assigned admin (by Telegram user ID) can access admin features.

---

## 🚀 Setup & Deployment

### 1. Requirements

- Python 3.8+
- PostgreSQL
- Bot token from [BotFather](https://t.me/BotFather)

### 2. Install dependencies

```bash
pip install aiogram psycopg2
