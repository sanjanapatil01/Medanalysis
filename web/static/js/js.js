let menuIcon =document.querySelector('#menu-icon');
let navbar =document.querySelector('.main-nav');
menuIcon.onclick=()=>{
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
}