document.addEventListener("DOMContentLoaded", function () {
    const burger = document.querySelector(".burger");
    const nav = document.querySelector(".nav-links");

    burger.addEventListener("click", () => {
        nav.classList.toggle("active");
        console.log("clicked");
    });
});