import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# セッション署名用の秘密鍵
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-this")

# ※簡易的なオンメモリデータベース（本番環境ではDBを使用してください）
users_db = {}
scores_db = [
    {"rank": 1, "name": "Alice", "score": 12500},
    {"rank": 2, "name": "Bob", "score": 9800},
    {"rank": 3, "name": "Charlie", "score": 7500},
]

# --- ホームページ ---
@app.route('/')
def index():
    return render_template('index.html')

# --- ユーザー登録画面 ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('ユーザー名とパスワードを入力してください。', 'danger')
            return redirect(url_for('register'))
            
        if username in users_db:
            flash('すでに使用されているユーザー名です。', 'danger')
            return redirect(url_for('register'))
            
        # パスワードを安全にハッシュ化して保存
        hashed_password = generate_password_hash(password)
        users_db[username] = hashed_password
        
        flash('登録が完了しました。ログインしてください。', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

# --- ログイン画面 ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_password = users_db.get(username)
        
        # ユーザーが存在し、パスワードが一致するか検証
        if user_password and check_password_hash(user_password, password):
            session['user'] = username
            flash('ログイン出来ました！', 'success')
            return redirect(url_for('index'))
        else:
            flash('ユーザー名またはパスワードが間違っています。', 'danger')
            
    return render_template('login.html')

# --- ログアウト ---
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('ログアウトしました。', 'info')
    return redirect(url_for('index'))

# --- スコアボード（ログイン必須） ---
@app.route('/scoreboard')
def scoreboard():
    # ログインしていなければログイン画面へリダイレクト
    if 'user' not in session:
        flash('スコアボードを利用するにはログインが必要です。', 'warning')
        return redirect(url_for('login'))
        
    return render_template('scoreboard.html', scores=scores_db)

if __name__ == '__main__':
    app.run(debug=True)
