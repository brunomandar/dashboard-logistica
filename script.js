function executarPython() {
  fetch("https://backend-python.onrender.com/executar")
    .then(resp => resp.json())
    .then(data => {
      document.getElementById("resultado").innerText = data.resultado;
    });
}