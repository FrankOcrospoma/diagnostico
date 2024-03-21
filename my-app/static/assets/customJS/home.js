const loaderOut = document.querySelector("#loader-out");
function fadeOut(element) {
  let opacity = 1;
  const timer = setInterval(function () {
    if (opacity <= 0.1) {
      clearInterval(timer);
      element.style.display = "none";
    }
    element.style.opacity = opacity;
    opacity -= opacity * 0.1;
  }, 50);
}
fadeOut(loaderOut);



function eliminarCategoria(id_categoria) {
  if (confirm("¿Estás seguro que deseas eliminar la categoría?")) {
    let url = `/borrar-categoria/${id_categoria}`;
    if (url) {
      window.location.href = url;
    }
  }
}
function eliminarNoticia(id_noticia) {
  if (confirm("¿Estás seguro que deseas eliminar la noticia?")) {
    let url = `/borrar-noticia/${id_noticia}`;
    if (url) {
      window.location.href = url;
    }
  }
}
function eliminarComentario(id_comentario) {
  if (confirm("¿Estás seguro que deseas eliminar el comentario?")) {
    let url = `/borrar-comentario/${id_comentario}`;
    if (url) {
      window.location.href = url;
    }
  }
}